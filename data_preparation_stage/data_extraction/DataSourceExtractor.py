from abc import ABC, abstractmethod

from data_objects import Document
from utils import LanguageHandler


class DataSourceExtractor(ABC):
    _language_handler: LanguageHandler

    def __init__(self):
        self._language_handler = LanguageHandler()

    @property
    def language_handler(self):
        return self._language_handler

    @abstractmethod
    def get_text(self, path: str) -> str:
        pass

    @abstractmethod
    def create_document(self, path: str) -> Document:
        pass

    @abstractmethod
    def divide_paragraphs(self, doc: Document, text: str) -> Document:
        pass