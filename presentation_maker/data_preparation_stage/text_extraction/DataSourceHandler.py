from presentation_maker.data_objects import Topic, Document
from presentation_maker.data_preparation_stage.text_extraction.WikipediaExtractor\
    import WikipediaExtractor
from presentation_maker.data_preparation_stage.text_extraction.PdfExtractor\
    import PdfExtractor
from presentation_maker.data_preparation_stage.text_extraction.WebExtractor\
    import WebExtractor
from presentation_maker.data_preparation_stage.text_extraction.Extractor \
    import Extractor
from presentation_maker.utils import is_path_or_url, download_to_working, copy_file_to_working, \
    InvalidPathError, get_file_name
from presentation_maker.utils.Errors import ExtractionError


class DataSourceHandler:
    WEB_EXTENSIONS: list[str]
    PDF_EXTENSIONS: list[str]

    def __init__(self):
        self.WEB_EXTENSIONS = ["html", "htm"]
        self.PDF_EXTENSIONS = ["pdf"]

    def create_document(self, extractor: Extractor, work_path: str
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

        if self.is_pdf(file_name):
            doc = self.create_document(PdfExtractor(), working_path, path)
        elif self.is_web_page(file_name):
            if path.find("wiki") != -1:
                doc = self.create_document(WikipediaExtractor(), working_path, path)
            else:
                doc = self.create_document(WebExtractor(), working_path, path)

        # add doc to Topic and return it.
        if doc is None:
            raise ExtractionError(file_name, path)
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
