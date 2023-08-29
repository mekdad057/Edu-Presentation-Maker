import re

from presentation_maker.data_objects import Document
from presentation_maker.data_preparation_stage.text_preprocessing.Processor \
    import Processor


@Processor.register_processor("new_lines_remover")
class NewLinesRemover(Processor):
    def process_document(self, doc: Document):
        for i in range(len(doc.paragraphs)):
            self._texts[i] = re.sub(r'[\n]+', ' ', self._texts[i])
            doc.paragraphs[i].processed_data = self._texts[i]


