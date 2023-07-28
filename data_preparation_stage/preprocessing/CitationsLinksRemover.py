import re

from data_objects import Document
from data_preparation_stage.preprocessing.DocumentProcessor \
    import DocumentProcessor


class CitationsLinksRemover(DocumentProcessor):
    def process_document(self, doc: Document):
        for i in range(len(self._texts)):
            self._texts[i] = re.sub(r'https?://S+', '', self._texts[i])
            self._texts[i] = re.sub(r'\[.*\]', '', self._texts[i])
            doc.paragraphs[i].processed_data = self._texts[i]
