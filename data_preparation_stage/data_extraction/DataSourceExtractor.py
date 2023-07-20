from abc import ABC, abstractmethod

from data_objects import Document
from utils import LanguageHandler


class DataSourceExtractor(ABC):
    __DATA_SOURCE_TYPE_NAME: str  # name of the extension of the file.
    _language_handler: LanguageHandler

    def __init__(self):
        self._language_handler = LanguageHandler()
        self.__DATA_SOURCE_TYPE_NAME = "Abstract Type"

    @property
    def DATA_SOURCE_TYPE_NAME(self):
        return self.__DATA_SOURCE_TYPE_NAME

    @property
    def language_handler(self):
        return self.language_handler

    @abstractmethod
    def get_text(self, path: str) -> str:
        pass

    @abstractmethod
    def create_document(self, path: str) -> Document:
        pass

    @abstractmethod
    def divide_paragraphs(self, doc: Document, text: str) -> Document:
        pass