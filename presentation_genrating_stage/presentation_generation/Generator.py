from abc import ABC, abstractmethod

from data_objects import Content


class Generator(ABC):
    _name: str

    @abstractmethod
    def get_output(self, params: dict[str, str]) -> Content:
        pass