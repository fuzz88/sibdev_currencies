import asyncio
from datetime import date
from typing import Set

import httpx

from .base import DataSource


class CBRFDaily(DataSource):
    RETRY_COUNT = 5

    @staticmethod
    async def fetch_archive(date: tuple) -> dict:
        """
        Идем за данными запросом HTTP GET.
        В случае нескольких неудачных попыток возвращаем объект с описанием ошибки.
        Все исключения транспорта обрабатываются внутри этой корутины.
        """
        year, month, day = date

        async def fetch(retry_count=CBRFDaily.RETRY_COUNT):
            try:
                url = f"https://www.cbr-xml-daily.ru/archive/{year}/{month:02}/{day:02}/daily_json.js"
                async with httpx.AsyncClient() as client:
                    resp = await client.get(url)
                    if resp.status_code != 200:
                        raise Exception(f"Retry. {resp.status_code} {url}")
                    return resp.json()
            except Exception as e:
                await asyncio.sleep(
                    (CBRFDaily.RETRY_COUNT + 1 - retry_count) * 1.0
                )  # progressive delay
                if retry_count == 0:
                    return {"error": (resp.status_code, date)}
                return await fetch(retry_count - 1)

        return await fetch()

    @staticmethod
    def get_updates(dates: Set[date]) -> list[dict]:
        """
        Закидываем список дат, для которых хотим получить данные, в корутины.
        Корутины асинхронно получают данные и обрабатывают ошибки сами.
        """
        fetching_tasks = asyncio.gather(
            *list(
                map(
                    CBRFDaily.fetch_archive,
                    (
                        (_.year, _.month, _.day) for _ in dates
                    ),  # simplify datatype for pass-by-value call
                )
            )
        )
        results = asyncio.get_event_loop().run_until_complete(fetching_tasks)
        return results
