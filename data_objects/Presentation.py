from data_objects.KeyPoint import KeyPoint
from data_objects.Script import Script
from data_objects.Slide import Slide


class Presentation:
    title: str
    all_keypoints: list[KeyPoint]
    all_scripts: list[Script]
    slides: list[Slide]
