from data_objects import Document
from data_preparation_stage.data_extraction.DataSourceExtractor\
    import DataSourceExtractor


class PdfExtractor(DataSourceExtractor):
    def __init__(self):
        super().__init__()

    def get_text(self, path: str) -> str:
        pass

    def get_paragraphs(self, doc: Document, text: str):
        pass
