from abc import ABC, abstractmethod

from data_objects import Document


class DocumentProcessor(ABC):
    _language: str
    _texts: list[str]

    def __init__(self):
        self._language = ""
        self._texts = []

    @abstractmethod
    def process_document(self, doc: Document):
        for p in doc.paragraphs:
            if p.processed_data == "":
                self._texts.append(p.raw_data)
            else:
                self._texts.append(p.processed_data)
        self._language = doc.language
