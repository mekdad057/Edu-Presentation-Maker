from datetime import datetime

from DataObjects.KeyPoint import KeyPoint
from DataObjects.Script import Script


class Slide:
    title: str
    number: int
    date: datetime
    keypoints: list[KeyPoint]
    script: Script
