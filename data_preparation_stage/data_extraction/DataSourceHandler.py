import os

from data_objects import Topic, Document
from data_preparation_stage.data_extraction.WikipediaExtractor\
    import WikipediaExtractor
from data_preparation_stage.data_extraction.DataSourceExtractor\
    import DataSourceExtractor
from data_preparation_stage.data_extraction.HtmlTrafilaturaExtractor import \
    HtmlTrafilaturaExtractor
from utils import is_path_or_url, download_to_working, copy_file_to_working, \
    InvalidPathError, get_file_name


class DataSourceHandler:

    def __init__(self):
        pass

    def create_document(self, extractor: DataSourceExtractor, path: str) \
            -> Document:
        return extractor.create_document(path)

    def add_source(self, topic: Topic, path: str):
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

        # use suitable extractor to create the content
        file_name = get_file_name(working_path)

        if self.is_pdf(file_name):
            pass  # todo : add pdf extractor
        elif self.is_web_page(file_name):
            # FIXME : this doesn't handle pages from other websites
            doc = self.create_document(WikipediaExtractor(), working_path)

        # add doc to Topic and return it.
        if doc is None:
            raise ValueError(f"Document '{file_name}' "
                             f"extraction FAILED")
            # todo: use a logger instead of printing messages.
        doc.path = path
        topic.documents.append(doc)

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
