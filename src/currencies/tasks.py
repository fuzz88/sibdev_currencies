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
    unsynced_dates = set([date.today() - timedelta(days=n) for n in range(31)]) - set(
        [
            CurrencyRate.objects.filter(
                date__gte=date.today() - timedelta(days=30)
            ).values_list("date")
        ]
    )
    print(f"unsynced_dates count: {len(unsynced_dates)}")
    return data_source.get_updates(unsynced_dates)


data_sources = [CBRFDaily]


@celery.task(bind=True)
def task_update_currencies_db(self):
    errors = []
    for ds in data_sources:
        try:
            results = get_unsynced_currencies_data(ds)
            print(f"got {len(results)} results.")
            for result in results:
                error = result.get("error")
                if error is None:
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
                        CurrencyRate(
                            cbrf_id=id,
                            num_code=num_code,
                            char_code=char_code,
                            name=name,
                            value=value,
                            previous_value=previous_value,
                            nominal=nominal,
                            date=date.split("T")[0],
                        ).save()
                else:
                    errors.append(error)
        except Exception as e:
            logging.getLogger().exception(e)
    if len(errors) != 0:
        # TODO:
        # error recovery plans:
        #   1. use values from next date values "previous_value" field.
        #   2. retry task in 10 minutes
        print(f"{len(errors)} errors: {errors}\n retry in 10 minutes?")
