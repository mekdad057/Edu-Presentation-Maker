from data_objects.Document import Document


class Topic:
    title: str
    document_subjects: dict[Document, int]
    documents: list[Document]

    def __init__(self):
        self.title = ""
        self.document_subjects = dict()
        self.documents = list()
