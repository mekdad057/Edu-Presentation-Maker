from presentation_maker.data_objects import Document
from presentation_maker.data_preparation_stage.text_extraction.Extractor \
    import Extractor


class PdfExtractor(Extractor):
    def __init__(self):
        super().__init__()

    def get_relevant_text(self, path: str) -> str:
        pass

    def get_paragraphs(self, doc: Document, text: str):
        pass
