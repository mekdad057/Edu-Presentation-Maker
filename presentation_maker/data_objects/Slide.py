from enum import Enum

from presentation_maker.data_objects.Content import Content
from presentation_maker.data_objects.KeyPoint import KeyPoint


class LAYOUT(Enum):
    """
    different layouts usually used in power-point presentations
    each has unique number
    """
    TITLE = 0
    TITLE_AND_CONTENT = 1
    PICTURE_CONTENT_WITH_CAPTION = 7


class Slide:
    title: str
    number: int
    _layout: LAYOUT
    keypoints: list[KeyPoint]
    content: Content

    def __init__(self, layout: LAYOUT):
        self.title = ""
        self.number = 0
        self.keypoints = list()
        self.script = None
        self._layout = layout

    @property
    def layout(self):
        return self._layout
