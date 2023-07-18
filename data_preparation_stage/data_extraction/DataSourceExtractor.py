from abc import ABC, abstractmethod

from data_objects import Document
from utils import LanguageHandler


class DataSourceExtractor(ABC):
    __DATA_SOURCE_TYPE_NAME: str  # name of the extension of the file.
    _language_handler: LanguageHandler

    def get_type(self) -> str:
        return self.__DATA_SOURCE_TYPE_NAME

    def get_langauge_handler(self) -> LanguageHandler:
        if self._language_handler is None:
            self._language_handler = LanguageHandler()
        return self._language_handler

    @abstractmethod
    def get_text(self, path: str) -> str:
        pass
