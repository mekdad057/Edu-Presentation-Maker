from data_objects import Document
from abc import ABC, abstractmethod


class DocumentProcessor(ABC):
    language: str
    INITIAL_PARAMS_VALUES: dict[str, str]

    @abstractmethod
    def process_text(self, doc: Document) -> Document:
        pass

    @abstractmethod
    def set_params(self, params: dict[str, str]):
        pass
