from data_objects.Content import Content
from data_objects.Document import Document


class KeyPoint(Content):

    def __init__(self, text: str, path: str):
        super().__init__(text, path)
