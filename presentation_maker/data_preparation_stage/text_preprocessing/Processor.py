from abc import ABC, abstractmethod

from presentation_maker.data_objects import Document


class Processor(ABC):
    _language: str
    _texts: list[str]
    _loaded: bool
    _registry = {}

    @classmethod
    def register_processor(cls, processor_name: str):
        def decorator(subclass):
            cls._registry[processor_name] = subclass
            return subclass
        return decorator

    @classmethod
    def registry(cls):
        return cls._registry

    def __init__(self):
        self._language = ""
        self._texts = []
        self._loaded = False

    def load_document(self, doc: Document):
        if not self._loaded:
            for p in doc.paragraphs:
                if p.processed_data == "":
                    self._texts.append(p.raw_data)
                else:
                    self._texts.append(p.processed_data)
            self._language = doc.language
            self._loaded = True

    @abstractmethod
    def process_document(self, doc: Document):
        pass

    def unload(self):
        self._texts = []
        self._loaded = False
