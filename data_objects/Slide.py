from datetime import datetime

from data_objects import KeyPoint, Script


class Slide:
    title: str
    number: int
    date: datetime
    keypoints: list[KeyPoint]
    script: Script
