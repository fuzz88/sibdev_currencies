import logging
from datetime import date, timedelta

from app.celery import celery
from currencies.data_sources.base import DataSource
from currencies.data_sources.CBRFDaily import CBRFDaily
from currencies.models import CurrencyRate


def get_unsynced_currencies_data(data_source: DataSource):
    """
    Обновляем данные валют по дням, которых еще нет в базе данных.
    """
    past_30days_dates = set([date.today() - timedelta(days=n) for n in range(31)])

    already_done = set(
        CurrencyRate.objects.filter(
            date__gte=date.today() - timedelta(days=30),
            char_code="GBP",  # можем использовать дату по одной валюте, так как из внешнего апи получаем сразу пачкой валют.
        )
        .distinct()  # debug. убрать
        .values_list("date", flat=True)
    )
    unsynced_dates = past_30days_dates.difference(already_done)
    # print(f"past_30days: {past_30days_dates}")
    # print(f"already done: {already_done}")
    # print(f"unsynced_dates: {unsynced_dates}")
    return data_source.get_updates(unsynced_dates)


data_sources = [CBRFDaily]  #  список источников данных


@celery.task(bind=True)
def task_update_currencies_db(self):
    """
    Пробегаемся по списку источников данных, у каждого запрашиваем данные.
    Каждый источник умеет
    """
    errors = []
    for ds in data_sources:
        try:
            # каждый элемент в списке results соответствует одной дате
            results = get_unsynced_currencies_data(ds)
            print(f"got {len(results)} results.")

            for result in results:
                # результатом может быть ошибка
                error = result.get("error")
                if error is None:
                    # ошибки нет, давайте парсить
                    date = result.get("Date")
                    valutes = result.get("Valute")
                    for valute in valutes.values():
                        id = valute.get("ID")
                        num_code = valute.get("NumCode")
                        char_code = valute.get("CharCode")
                        name = valute.get("Name")
                        value = valute.get("Value")
                        previous_value = valute.get("Previous")
                        nominal = valute.get("Nominal")
                        # отпарсили без ошибок, ок, сохраняем
                        CurrencyRate(
                            cbrf_id=id,
                            num_code=num_code,
                            char_code=char_code,
                            name=name,
                            value=value,
                            previous_value=previous_value,
                            nominal=nominal,
                            date=date.split("T")[0],  # отрезаем время
                        ).save()
                else:
                    # если результатом запроса по дате вернулась ошибка,
                    errors.append(error)
        except Exception as e:
            # если что-то поломалось на нашей стороне, то запишем в логи.

            # ошибки транспорта мы обработали в месте его использования.
            logging.getLogger().exception(e)
    if len(errors) != 0:
        # если ошибку возвращает внешнее апи, то делаем ретрай всей celery task
        # для всех несинхронизированных из-за этих ошибок дат.
        # TODO:
        # error recovery plans:
        #   1. use values from next date values "previous_value" field.
        #   2. retry task in 10 minutes
        print(f"{len(errors)} errors: {errors}\n retry in 10 minutes?")
