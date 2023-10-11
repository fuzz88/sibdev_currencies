import logging
from datetime import date, timedelta

from app.celery import celery
from currencies.data_sources.base import DataSource
from currencies.data_sources.CBRFDaily import CBRFDaily
from currencies.models import Currency, CurrencyRate


def get_unsynced_currencies_data(data_source: DataSource) -> list[dict]:
    """
    Обновляем данные валют по дням, которых еще нет в базе данных.
    """
    past_30days_dates = set([date.today() - timedelta(days=n) for n in range(31)])

    already_done = set(
        CurrencyRate.objects.filter(
            date__gte=date.today() - timedelta(days=30),
        )
        .values_list("date", flat=True)
        .distinct()
    )
    unsynced_dates = past_30days_dates.difference(already_done)
    # print(f"past_30days: {past_30days_dates}")
    # print(f"already done: {already_done}")
    # print(f"unsynced_dates: {unsynced_dates}")
    return data_source.get_updates(unsynced_dates)


@celery.task(bind=True)
def task_update_currencies_db(self):
    """
    Пробегаемся по списку источников данных, у каждого запрашиваем данные.
    """
    data_sources = [CBRFDaily]  #  список источников данных
    errors = []
    for ds in data_sources:
        try:
            # каждый элемент в списке results соответствует одной дате
            results: list = get_unsynced_currencies_data(ds)

            # подтянем список известных нам валют в словарь
            # используем его при парсинге, чтобы лишний раз не бегать в базу данных
            # за айди объекта валюты при записи обновления её рэйта.
            currencies = dict(Currency.objects.all().values_list("char_code", "id"))

            for result in results:
                # результатом может быть ошибка
                error = result.get("error")
                if error is None:
                    # ошибки нет, давайте парсить
                    date = result.get("Date")

                    # основной словарь с валютами. такой вот примерно:
                    # {
                    #     "GBP": {
                    #         "Value": 1.0,
                    #         "CharCode": "GBP",
                    #         ...
                    #     }
                    # }
                    # ключ, как видим, можем не итерировать - он дублируется.

                    valutes = result.get("Valute")
                    for valute in valutes.values():
                        id = valute.get("ID")
                        num_code = valute.get("NumCode")
                        char_code = valute.get("CharCode")
                        name = valute.get("Name")
                        value = valute.get("Value")
                        prev_value = valute.get("Previous")
                        nominal = valute.get("Nominal")

                        # проверяем, известна ли нам была валюта в момент запуска таски
                        currency_object_id = currencies.get(char_code)

                        if currency_object_id is None:
                            # нет, не известна. 
                            # скорее всего, это первый запуск таски, т.н. "прогрев"
                            # делаем запрос в б.д.
                            currency_object, _ = Currency.objects.get_or_create(
                                cbrf_id=id,
                                num_code=num_code,
                                char_code=char_code,
                                name=name,
                                nominal=nominal,
                            )
                            currency_object_id = currency_object.id
                        # отпарсили без ошибок, ок, сохраняем
                        CurrencyRate(
                            currency_id=currency_object_id,
                            value=value,
                            prev_value=prev_value,
                            date=date.split("T")[0],  # отрезаем время
                        ).save()
                else:
                    # если результатом запроса по дате вернулась ошибка,
                    errors.append(error)
        except Exception as e:
            # если что-то поломалось на нашей стороне, то запишем в логи.
            # например, формат данных изменился, у нас сломался парсинг.
            # или мы потеряли коннект в бд.

            # ошибки транспорта мы обработали в месте его использования.
            logging.getLogger().exception(e)
    if len(errors) != 0:
        # если ошибку возвращает внешнее апи, то делаем ретрай всей celery task
        # для всех несинхронизированных из-за этих ошибок дат.
        # TODO:
        # error recovery plans:
        #   1. use values from next date values "previous_value" field.
        #   2. retry task in 10 minutes
        logging.getLogger().error(
            f"{len(errors)} errors: {errors}\n retry in 10 minutes? 120 minutes?"
        )
