from abc import ABC, abstractmethod

from presentation_maker.data_objects import Document
from presentation_maker.utils import get_file_name


class Extractor(ABC):

    @abstractmethod
    def get_relevant_text(self, path: str) -> str:
        pass

    def create_document(self, work_path: str, real_path: str) -> Document:
        # 1) extracting main content from the page
        contents = self.get_relevant_text(work_path)

        # 2) evaluating attributes
        name = self._get_doc_name(work_path)
        language = "english"

        # 3) creating Document Object with the attributes
        doc = Document(name, real_path, language)

        # 4) dividing the extracted content to paragraphs
        self.get_paragraphs(doc, contents)

        return doc

    @abstractmethod
    def get_paragraphs(self, doc: Document, text: str):
        pass

    @abstractmethod
    def _get_doc_name(self, work_path) -> str:
        return get_file_name(work_path)
