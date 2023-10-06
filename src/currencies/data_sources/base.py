from abc import ABCMeta, abstractmethod


class DataSource(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_updates():
        pass
