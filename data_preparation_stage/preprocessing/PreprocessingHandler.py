from data_objects import Document, Topic
from .DocumentProcessor import DocumentProcessor


class PreprocessingHandler:
    def process(self, topic: Topic, documents_names: list[str]
                , processing_methods_names: list[str]
                , params: dict[str, str]) -> Topic:
        # todo : how to pass and deal with params
        pass

    def process_document(self, processor: DocumentProcessor, document_name: str
                         , params: dict[str, str]) -> Document:
        pass

    def get_processor(self, name: str) -> DocumentProcessor:
        pass
