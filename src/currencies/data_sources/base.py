from abc import ABCMeta, abstractmethod
from datetime import date
from typing import Set


class DataSource(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_updates(dates: Set[date]) -> list[dict]:
        pass
