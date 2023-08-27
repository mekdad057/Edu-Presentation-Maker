from presentation_maker.data_objects.Paragraph import Paragraph
from presentation_maker.data_objects.Content import Content


class KeyPoint(Content):
    """
    an extracted or generated sentence that will be turned to a bullet point
     later in the slide.
    """
    _level: int

    def __init__(self, text: str, reference: Paragraph, level: int = -1):
        super().__init__(text, reference)
        self._level = level

    @property
    def level(self):
        return self._level
