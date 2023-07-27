from data_objects import Presentation, Topic, Slide


class Organizer:

    def __init__(self):
        pass

    def organize(self, presentation: Presentation, topic: Topic
                 , slides_number: int):
        if slides_number == -1:
            num = 1
            for slide_keypoints in presentation.all_keypoints:
                source_paragraph = slide_keypoints[0].reference
                title = source_paragraph.raw_data.strip().split('|')[0]
                slide = Slide()
                slide.title = title
                slide.keypoints = slide_keypoints
                slide.number = num
                num += 1
                presentation.slides.append(slide)

