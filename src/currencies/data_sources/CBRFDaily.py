import asyncio
from datetime import date
from typing import Set

import httpx

from .base import DataSource


class CBRFDaily(DataSource):
    @staticmethod
    async def fetch_archive(date: tuple) -> dict:
        year, month, day = date
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://www.cbr-xml-daily.ru/archive/{year}/{month:02}/{day:02}/daily_json.js"
            )
            return resp.json()

    @staticmethod
    def get_updates(dates: Set[date]):
        """
        asyncroniously fetch archive for past 30 days and return results when all ready.
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
