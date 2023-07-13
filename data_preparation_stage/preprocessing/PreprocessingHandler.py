from data_objects import Topic, Document
from data_preparation_stage.preprocessing import DocumentProcessor


class PreprocessingHandler:
    def process(self, topic: Topic, documents_names: list[str]
                , processing_methods_names: list[str]
                , params: dict[str, str]) -> Topic:
        # todo : how to pass and deal with params, what is the format?
        pass

    def process_document(self, processor: DocumentProcessor, document: Document
                         , params: dict[str, str]) -> Document:
        pass

    def get_processor(self, name: str) -> DocumentProcessor:
        pass
