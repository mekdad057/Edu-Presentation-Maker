from data_objects.Content import Content
from data_objects.KeyPoint import KeyPoint
from data_objects.Script import Script
from data_objects.Slide import Slide


class Presentation:
    title: str
    all_keypoints: list[list[KeyPoint]]  # a list for each slide
    all_scripts: list[Script]
    all_content: list[Content]
    slides: list[Slide]

    def __init__(self):
        self.title = ""
        self.all_keypoints = list()
        self.all_scripts = list()
        self.slides = list()
        self.all_content = list()
