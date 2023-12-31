import logging

from presentation_maker.data_objects import Topic, Document
from presentation_maker.data_preparation_stage.text_extraction import DataSourceHandler
from presentation_maker.data_preparation_stage.text_preprocessing import PreprocessingHandler
from presentation_maker.utils.Errors import NotFoundError


class TopicHandler:
    _topic: Topic
    _datasource_handler: DataSourceHandler
    _processing_handler: PreprocessingHandler

    def __init__(self, title: str = ""):
        self._topic = Topic(title)
        self._datasource_handler = DataSourceHandler()
        self._processing_handler = PreprocessingHandler()

    @property
    def topic(self):
        return self._topic

    def reset(self, title: str = ""):
        self._topic = Topic(title)

    def add_source(self, path: str) -> bool:
        try:
            self._datasource_handler.add_source(self.topic, path)

            # setting the subject for the document inside the documents_subjects
            # dictionary in topic object.
            topic_subjects = self.topic.document_subjects
            subject = len(topic_subjects) + 1
            for doc in self.topic.documents:
                if doc.path == path:
                    topic_subjects[doc] = subject
                break
            return True
        except Exception as e:
            logging.exception(e)
            return False

    def add_sources(self, paths: list[str], same_subject: bool = False) -> bool:
        try:
            for path in paths:
                self._datasource_handler.add_source(self.topic, path)
                pass

            # setting the subject for the document inside the documents_subjects
            # dictionary in topic object.
            topic_subjects = self.topic.document_subjects
            subject = len(topic_subjects)+1
            for doc in self.topic.documents:
                if doc.path in paths:
                    topic_subjects[doc] = subject
                    # this line makes sure that documents that don't have the
                    # same subject has different values
                    subject += int(not same_subject)
            return True
        except Exception as e:
            logging.exception(e)
            return False

    def start_preprocessing(self, document_names: list[str]
                            , processing_methods_names: list[str]) -> bool:
        try:
            # getting all the documents that need text_preprocessing
            docs = []
            for name in document_names:
                doc = self.get_document(name)
                if doc is None:
                    raise NotFoundError("document", name)
                else:
                    docs.append(doc)
            ###
            self._processing_handler.process(docs, processing_methods_names)
            return True
        except Exception as e:
            logging.exception(e)
            return False

    def get_document(self, document_name: str) -> Document:
        doc = None
        for d in self.topic.documents:
            if d.name == document_name:
                doc = d
                break
        return doc
