import logging

from bs4 import BeautifulSoup

from data_objects import Document
from data_preparation_stage.data_extraction.DataSourceExtractor\
    import DataSourceExtractor


class WebExtractor(DataSourceExtractor):
    def get_text(self, path: str) -> str:
        try:
            with open(path, 'rb') as f:
                data = f.read()
        except Exception as e:
            logging.debug("Couldn't read file in Extractor.")
            raise e

        from readability import Document

        doc = Document(data)
        content_html = doc.summary()
        soup = BeautifulSoup(content_html, 'lxml')

        return soup.__unicode__()

    def get_paragraphs(self, doc: Document, text: str):
        pass

