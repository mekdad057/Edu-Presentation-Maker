from DataObjects.KeyPoint import KeyPoint
from DataObjects.Script import Script
from DataObjects.Slide import Slide


class Presentation:
    title: str
    all_keypoints: list[KeyPoint]
    all_scripts: list[Script]
    slides: list[Slide]
