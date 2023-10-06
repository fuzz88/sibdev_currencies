import logging

from app.celery import celery
from currencies.data_sources.base import DataSource
from currencies.data_sources.CBRFDaily import CBRFDaily


def handle_update(data_source: DataSource):
    data_source.get_updates()


data_sources = [CBRFDaily]


@celery.task
def task_update_currencies_db():
    for ds in data_sources:
        try:
            handle_update(ds)
        except Exception as e:
            logging.getLogger().exception(e)
