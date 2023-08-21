from presentation_maker.data_objects.Document import Document


class Topic:
    title: str
    document_subjects: dict[Document, int]
    documents: list[Document]

    def __init__(self, title: str = ""):
        self.title = title
        self.document_subjects = dict()
        self.documents = list()
