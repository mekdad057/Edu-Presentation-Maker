from presentation_maker.data_objects.Paragraph import Paragraph


class Document:
    name: str
    path: str
    language: str
    paragraphs: list[Paragraph]

    def __init__(self, name: str, path: str, language: str = "en"):
        self.name = name
        self.path = path
        self.language = language
        self.paragraphs = list()
