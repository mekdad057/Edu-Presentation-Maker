from abc import ABC, abstractmethod

from data_objects import Document
from utils import LanguageHandler, get_file_name


class DataSourceExtractor(ABC):
    _language_handler: LanguageHandler

    def __init__(self):
        self._language_handler = LanguageHandler()

    @property
    def language_handler(self):
        return self._language_handler

    @abstractmethod
    def get_text(self, path: str) -> str:  # todo: rename this method
        pass

    def create_document(self, work_path: str, real_path: str) -> Document:
        # 1) extracting main content from the page
        contents = self.get_text(work_path)

        # 2) evaluating attributes
        name = get_file_name(work_path)
        language = self.language_handler.determine_language(contents)

        # 3) creating Document Object with the attributes
        doc = Document(name, real_path, language)

        # 4) dividing the extracted content to paragraphs
        self.get_paragraphs(doc, contents)

        return doc

    @abstractmethod
    def get_paragraphs(self, doc: Document, text: str):
        pass
