from presentation_maker.data_objects import Document
from presentation_maker.data_preparation_stage.text_preprocessing.Processor \
    import Processor


class RepeatedWordsRemover(Processor):
    def process_document(self, doc: Document):
        for i in range(len(doc.paragraphs)):
            words = self._texts[i].split()
            res = []
            prev = ""
            for w in words:
                if w != prev:
                    res.append(w)
                prev = w
            doc.paragraphs[i].processed_data = " ".join(res)
