from data_objects import Topic, Document
from data_preparation_stage.data_extraction import DataSourceHandler
from data_preparation_stage.preprocessing import PreprocessingHandler


class TopicHandler:
    _topic: Topic
    _datasource_handler: DataSourceHandler
    _processing_handler: PreprocessingHandler

    def __init__(self):
        self._topic = Topic()
        self._datasource_handler = DataSourceHandler()
        self._processing_handler = PreprocessingHandler()

    @property
    def topic(self):
        return self._topic

    @property
    def datasource_handler(self):
        return self._datasource_handler

    @property
    def processing_handler(self):
        return self._processing_handler

    def reset(self):
        self._topic = Topic()

    def add_source(self, path: str) -> bool:
        pass

    def add_sources(self, paths: list[str], same_subject: bool = False) -> bool:
        pass

    def start_preprocessing(self, document_names: list[str]
                            , processing_methods_names: list[str]
                            , params: dict[str, object]) -> bool:
        pass

    def get_document(self, document_name: str) -> Document:
        doc = None
        for d in self.topic.documents:
            if d.name == document_name:
                doc = d
                break
        return doc
