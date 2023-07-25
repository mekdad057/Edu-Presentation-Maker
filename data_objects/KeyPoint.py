from data_objects.Paragraph import Paragraph
from data_objects.Content import Content

class KeyPoint(Content):

    def __init__(self, text: str, reference: Paragraph):
        super().__init__(text, reference)
