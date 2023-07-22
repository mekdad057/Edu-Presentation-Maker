import re

from data_objects import Document
from data_preparation_stage.preprocessing.DocumentProcessor\
    import DocumentProcessor


class Normalizer(DocumentProcessor):

    def __init__(self):
        super().__init__()

    def process_document(self, doc: Document):
        super().process_document(doc)
        for i in range(len(doc.paragraphs)):
            if self._language == "en":
                doc.paragraphs[i].processed_data = self._texts[i].lower()
            elif self._language == "ar":
                doc.paragraphs[i].processed_data =\
                    self.normalize_arabic(self._texts[i])

    def normalize_arabic(self, text) -> str:
        text = re.sub("[إأآا]", "ا", text)
        text = re.sub("ى", "ي", text)
        text = re.sub("ؤ", "ء", text)
        text = re.sub("ئ", "ء", text)
        text = re.sub("ة", "ه", text)
        text = re.sub("گ", "ك", text)
        return text
