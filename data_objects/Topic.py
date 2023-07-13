from data_objects import Document


class Topic:
    title: str
    document_subjects: dict[Document, int]
    documents: list[Document]
