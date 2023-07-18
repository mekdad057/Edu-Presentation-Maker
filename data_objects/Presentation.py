from data_objects.KeyPoint import KeyPoint
from data_objects.Script import Script
from data_objects.Slide import Slide


class Presentation:
    title: str
    all_keypoints: list[KeyPoint]
    all_scripts: list[Script]
    slides: list[Slide]

    def __init__(self):
        self.title = ""
        self.all_keypoints = list()
        self.all_scripts = list()
        self.slides = list()
