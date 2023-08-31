from presentation_maker.data_objects import Presentation, Topic, Slide, Paragraph, LAYOUT, Image


class Organizer:
    _NUM_KEY_POINTS_PER_SLIDE: int

    def __init__(self):
        self._NUM_KEY_POINTS_PER_SLIDE = 4

    def organize(self, presentation: Presentation, topic: Topic
                 , slides_number: int):
        if slides_number == -1:
            num = 1
            for group_keypoints in presentation.all_keypoints:
                source_paragraph: Paragraph = group_keypoints[0].reference
                slide = None
                for i in range(len(group_keypoints)):
                    if i % self._NUM_KEY_POINTS_PER_SLIDE == 0:
                        # adds slide if previous slide to the deck
                        if slide is not None:
                            presentation.slides.append(slide)
                        # choosing the right layout for the slide
                        # working with the rule:
                        # match each paragraph with a slide
                        slide = self.__choose_layout(source_paragraph, num)
                        num += 1
                    slide.keypoints.append(group_keypoints[i])

                presentation.slides.append(slide)

    def __choose_layout(self, source_paragraph: Paragraph, number: int) -> Slide:
        slide = None
        if len(source_paragraph.contents_paths) > 0:
            slide = Slide(LAYOUT.PICTURE_CONTENT_WITH_CAPTION)
        else:
            slide = Slide(LAYOUT.TITLE_AND_CONTENT)
        for path in source_paragraph.contents_paths:
            slide.content = Image(path, slide)
        slide.title = source_paragraph.title
        slide.number = number
        return slide
