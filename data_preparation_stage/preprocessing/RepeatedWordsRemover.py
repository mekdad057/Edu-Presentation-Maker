from data_objects import Document
from data_preparation_stage.preprocessing.DocumentProcessor\
    import DocumentProcessor


class RepeatedWordsRemover(DocumentProcessor):
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
