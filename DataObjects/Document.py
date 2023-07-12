from DataObjects.Paragraph import Paragraph


class Document:
    _size: int
    name: str
    path: str
    language: str
    paragraphs: list[Paragraph]
