from data_objects.Content import Content
from data_objects.Document import Document


class Script(Content):
    reference: str

    def __init__(self, text, path):
        super().__init__(text, path)

