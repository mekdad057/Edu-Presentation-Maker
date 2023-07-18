from data_objects import Topic, Document
from data_preparation_stage.data_extraction import DataSourceExtractor


class DataSourceHandler:

    def __init__(self):
        pass

    def create_document(self, extractor: DataSourceExtractor, path: str) \
            -> Document:
        pass

    def add_source(self, topic: Topic, path: str) -> Topic:
        pass

    def is_pdf(self, path: str) -> bool:
        pass

    def is_web_page(self, path: str) -> bool:
        pass
