from data_objects.Document import Document
from data_objects.Topic import Topic
from data_preparation_stage.data_extraction.DataSourceExtractor import DataSourceExtractor


class DataSourceHandler:
    def create_document(self, extractor: DataSourceExtractor, path: str) -> Document:
        pass

    def add_source(self, topic: Topic, path: str) -> Topic:
        pass

    def is_pdf(self, path: str) -> bool:
        pass

    def is_web_page(self, path: str) -> bool:
        pass
