from abc import ABC, abstractmethod

from data_objects import Document


class DocumentProcessor(ABC):
    language: str
    _current_params_values: dict[str, object]
    INITIAL_PARAMS_VALUES: dict[str, object]

    @abstractmethod
    def process_text(self, doc: Document) -> Document:
        pass

    @abstractmethod
    def set_params(self, params: dict[str, object]):
        # Here we have to check if the parameters actually belong to the
        # processor
        pass
