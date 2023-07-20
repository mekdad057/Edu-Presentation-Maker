import os

from data_objects import Topic, Document
from data_preparation_stage.data_extraction import DataSourceExtractor
from utils import is_path_or_url, download_to_working, copy_file_to_working, \
    InvalidPathError


class DataSourceHandler:

    def __init__(self):
        pass

    def create_document(self, extractor: DataSourceExtractor, path: str) \
            -> Document:
        pass

    def add_source(self, topic: Topic, path: str) -> Topic:
        doc = None

        # move the file to working directory
        type_of_path = is_path_or_url(path)
        working_path = ""

        if type_of_path == 'URL':
            working_path = download_to_working(path)
        elif type_of_path == 'Path':
            working_path = copy_file_to_working(path)
        else:
            raise InvalidPathError(f"path: {path}:\nis invalid")
        # use the suitable extractor
        file_name = working_path.split(os.path.sep)[-1]

        if self.is_pdf(file_name):
            pass
        elif self.is_web_page(file_name):
            pass
            # doc = self.create_document(ex, working_path)
            # todo: come here and complete the extraction code.

        # add doc to Topic and return it.
        if doc is None:
            raise ValueError(f"Document '{file_name}' "
                             f"extraction FAILED")
            # todo: use a logger instead of printing messages.
        doc.path = path
        topic.documents.append(doc)
        return topic

    @staticmethod
    def is_pdf(name: str) -> bool:
        return False

    @staticmethod
    def is_web_page(name: str) -> bool:
        extensions = ['html', 'htm']
        if name.split('.')[-1] in extensions:
            return True
        else:
            return False
