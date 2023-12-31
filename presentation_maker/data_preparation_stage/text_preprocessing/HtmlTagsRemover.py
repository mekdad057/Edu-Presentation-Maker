import re

from presentation_maker.data_objects import Document
from presentation_maker.data_preparation_stage.text_preprocessing.Processor \
    import Processor


@Processor.register_processor("html_tags_remover")
class HtmlTagsRemover(Processor):

    def process_document(self, doc: Document):
        for i in range(len(self._texts)):
            self._texts[i] = re.sub(r"<.*?>", "", self._texts[i])
            doc.paragraphs[i].processed_data = self._texts[i]


