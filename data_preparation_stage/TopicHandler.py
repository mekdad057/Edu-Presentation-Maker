from data_objects import Topic, Document
from data_preparation_stage.data_extraction import DataSourceHandler
from data_preparation_stage.preprocessing import PreprocessingHandler


class TopicHandler:
    _topic: Topic
    _datasource_handler: DataSourceHandler
    _processing_handler: PreprocessingHandler

    def get_processing_handler(self):
        if self._processing_handler is None:
            self._processing_handler = PreprocessingHandler()
        return self._processing_handler

    def get_data_handler(self):
        if self._datasource_handler is None:
            self._datasource_handler = DataSourceHandler()
        return self._datasource_handler

    def add_source(self, path: str) -> bool:
        pass

    def add_sources(self, paths: list[str], same_subject: bool = False) -> bool:
        pass

    def start_preprocessing(self, document_names: list[str]
                            , processing_methods_names: list[str]
                            , params: dict[str, object]) -> bool:
        pass

    def get_topic(self):
        if self._topic is None:
            self._topic = Topic()
        return self._topic

    def get_document(self, document_name: str) -> Document:
        pass
