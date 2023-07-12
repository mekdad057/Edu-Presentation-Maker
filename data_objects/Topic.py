from data_objects.Document import Document


class Topic:
    title: str
    document_subjects: dict[str, int]
    documents: list[Document]
