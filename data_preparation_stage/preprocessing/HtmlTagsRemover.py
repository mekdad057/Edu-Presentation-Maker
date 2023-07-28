import re

from data_objects import Document
from data_preparation_stage.preprocessing.DocumentProcessor\
    import DocumentProcessor


class HtmlTagsRemover(DocumentProcessor):
    def process_document(self, doc: Document):
        super().process_document(doc)
        for i in range(len(self._texts)):
            self._texts[i] = re.sub(r"<.*?>", "", self._texts[i])
            doc.paragraphs[i].processed_data = self._texts[i]


