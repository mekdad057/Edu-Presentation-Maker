from data_objects import KeyPoint, Script, Slide


class Presentation:
    title: str
    all_keypoints: list[KeyPoint]
    all_scripts: list[Script]
    slides: list[Slide]
