from datetime import datetime

from data_objects.KeyPoint import KeyPoint
from data_objects.Script import Script


class Slide:
    title: str
    number: int
    date: datetime
    keypoints: list[KeyPoint]
    script: Script

    def __init__(self):
        self.title = ""
        self.number = 0
        self.date = datetime.now()
        self.keypoints = list()
        self.script = None