from data_objects import Topic, Document
from data_preparation_stage.data_extraction import DataSourceHandler
from data_preparation_stage.preprocessing import PreprocessingHandler
from utils.Errors import NotFoundError


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
        try:
            self.datasource_handler.add_source(self.topic, path)

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
            print(e)
            return False

    def add_sources(self, paths: list[str], same_subject: bool = False) -> bool:
        try:
            for path in paths:
                self.datasource_handler.add_source(self.topic, path)
                pass

            # setting the subject for the document inside the documents_subjects
            # dictionary in topic object.
            topic_subjects = self.topic.document_subjects
            subject = len(topic_subjects)+1
            for doc in self.topic.documents:
                if doc.path in paths:
                    topic_subjects[doc] = subject
                    # this line makes sure that documents that has the same
                    # subject has the same value
                    subject += int(not same_subject)
            return True
        except Exception as e:
            print(e)
            return False

    def start_preprocessing(self, document_names: list[str]
                            , processing_methods_names: list[str]) -> bool:
        try:
            # getting all the documents that need preprocessing
            docs = []
            for name in document_names:
                doc = self.get_document(name)
                if doc is None:
                    raise NotFoundError(f"Document with name {name}"
                                                f" not found")
                else:
                    docs.append(doc)
            ###
            self.processing_handler.process(docs, processing_methods_names)
            return True
        except Exception as e:
            print(e)
            return False

    def get_document(self, document_name: str) -> Document:
        doc = None
        for d in self.topic.documents:
            if d.name == document_name:
                doc = d
                break
        return doc
