import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

from app.conf.environ import env

__all__ = [
    "celery",
]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

celery = Celery("tasks")

celery.conf.update(
    broker_url=env("CELERY_BROKER_URL"),
    task_always_eager=env(
        "CELERY_ALWAYS_EAGER", cast=bool, default=settings.DEBUG
    ),  # by default in debug mode we run all celery tasks in foregroud.
    task_eager_propagates=True,
    task_ignore_result=True,
    task_store_errors_even_if_ignored=True,
    task_acks_late=True,
    timezone=env("TIME_ZONE", cast=str, default="Europe/Moscow"),
    enable_utc=False,
    beat_schedule={
        "update_currencies_db": {
            "task": "currencies.tasks.task_update_currencies_db",
            "schedule": crontab(hour="*", minute="*/1"),
        },
    },
)


celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
