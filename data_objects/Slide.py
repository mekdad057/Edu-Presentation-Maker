from data_objects.KeyPoint import KeyPoint
from data_objects.Script import Script


class Slide:
    title: str
    number: int
    keypoints: list[KeyPoint]
    script: Script

    def __init__(self):
        self.title = ""
        self.number = 0
        self.keypoints = list()
        self.script = None
