from datetime import datetime

from data_objects.KeyPoint import KeyPoint
from data_objects.Script import Script


class Slide:
    title: str
    number: int
    date: datetime
    keypoints: list[KeyPoint]
    script: Script
