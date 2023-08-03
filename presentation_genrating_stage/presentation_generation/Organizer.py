from data_objects import Presentation, Topic, Slide


class Organizer:
    _NUM_KEY_POINTS_PER_SLIDE: int
    _WORDS_LIMIT: int

    def __init__(self):
        self._NUM_KEY_POINTS_PER_SLIDE = 4
        self._WORDS_LIMIT = 15

    def organize(self, presentation: Presentation, topic: Topic
                 , slides_number: int):
        if slides_number == -1:
            num = 1
            for group_keypoints in presentation.all_keypoints:
                source_paragraph = group_keypoints[0].reference
                slide = None
                for i in range(len(group_keypoints)):
                    if i % self._NUM_KEY_POINTS_PER_SLIDE == 0:
                        if slide is not None:
                            presentation.slides.append(slide)
                        slide = Slide()
                        slide.title = source_paragraph.title
                        slide.number = num
                        num += 1
                    slide.keypoints.append(group_keypoints[i])

                presentation.slides.append(slide)

