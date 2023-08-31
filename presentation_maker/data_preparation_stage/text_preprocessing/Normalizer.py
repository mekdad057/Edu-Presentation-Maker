import re

from presentation_maker.data_objects import Document
from presentation_maker.data_preparation_stage.text_preprocessing.Processor \
    import Processor


@Processor.register_processor("normalizer")
class Normalizer(Processor):
    def process_document(self, doc: Document):
        for i in range(len(doc.paragraphs)):
            if self._language == "en":
                doc.paragraphs[i].processed_data = self._texts[i].lower()
            elif self._language == "ar":
                doc.paragraphs[i].processed_data =\
                    self._normalize_arabic(self._texts[i])

    def _normalize_arabic(self, text) -> str:
        text = re.sub("[إأآا]", "ا", text)
        text = re.sub("ى", "ي", text)
        text = re.sub("ؤ", "ء", text)
        text = re.sub("ئ", "ء", text)
        text = re.sub("ة", "ه", text)
        text = re.sub("گ", "ك", text)
        return text
