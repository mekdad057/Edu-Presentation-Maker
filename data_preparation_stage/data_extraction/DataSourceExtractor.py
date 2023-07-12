from data_objects.Document import Document
from abc import ABC, abstractmethod


class DataSourceExtractor(ABC):
    __DATA_SOURCE_TYPE_NAME: str
    # todo : How to add the language Handler with less dependency.
    def get_type(self) -> str:
        return self.__DATA_SOURCE_TYPE_NAME

    @abstractmethod
    def get_text(self, path: str) -> Document:
        pass
