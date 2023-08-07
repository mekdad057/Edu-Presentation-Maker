from enum import Enum, auto

from data_objects.Content import Content
from data_objects.KeyPoint import KeyPoint
from data_objects.Script import Script


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
    script: Script
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
