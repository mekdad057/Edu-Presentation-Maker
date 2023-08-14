import os

from data_objects import Topic, Document
from data_preparation_stage.data_extraction.PdfExtractor import PdfExtractor
from data_preparation_stage.data_extraction.WebExtractor import WebExtractor
from data_preparation_stage.data_extraction.WikipediaExtractor\
    import WikipediaExtractor
from data_preparation_stage.data_extraction.DataSourceExtractor\
    import DataSourceExtractor
from data_preparation_stage.data_extraction.HtmlTrafilaturaExtractor import \
    HtmlTrafilaturaExtractor
from utils import is_path_or_url, download_to_working, copy_file_to_working, \
    InvalidPathError, get_file_name


class DataSourceHandler:
    WEB_EXTENSIONS: list[str]
    PDF_EXTENSIONS: list[str]

    def __init__(self):
        self.WEB_EXTENSIONS = ["html", "htm"]
        self.PDF_EXTENSIONS = ["pdf"]

    def create_document(self, extractor: DataSourceExtractor, work_path: str
                        , real_path: str) -> Document:
        return extractor.create_document(work_path, real_path)

    def add_source(self, topic: Topic, path: str):
        doc = None

        # move the file to working directory
        type_of_path = is_path_or_url(path)

        if type_of_path == 'URL':
            working_path = download_to_working(path)
        elif type_of_path == 'Path':
            working_path = copy_file_to_working(path)
        else:
            raise InvalidPathError(f"path: {path}:\nis invalid")

        # use suitable extractor to create the content
        file_name = get_file_name(working_path)

        # todo : how to select depending on path?
        if self.is_pdf(file_name):
            doc = self.create_document(PdfExtractor(), working_path, path)
        elif self.is_web_page(file_name):
            doc = self.create_document(WebExtractor(), working_path, path)

        # add doc to Topic and return it.
        if doc is None:
            raise ValueError(f"Document '{file_name}' "
                             f"extraction FAILED")
        doc.path = path  # fixme : is this ok?
        topic.documents.append(doc)

    def is_pdf(self, name: str) -> bool:
        if name.split('.')[-1] in self.PDF_EXTENSIONS:
            return True
        else:
            return False

    def is_web_page(self, name: str) -> bool:
        if name.split('.')[-1] in self.WEB_EXTENSIONS:
            return True
        else:
            return False
