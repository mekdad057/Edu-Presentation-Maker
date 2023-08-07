import copy
import logging
import os.path

import pptx
from pptx.util import Pt

from data_objects import Presentation, Topic, LAYOUT
from presentation_genrating_stage.presentation_generation import \
    GenerationHandler, Organizer
from templates import TEMPLATE
from utils import RESULTS_DIR
from utils.Errors import NotFoundError
from utils.PresentationExportionUtils import replace_with_image, \
    CONTENT_PLACEHOLDER_IDX, DEFAULT_BULLET_POINT_FONT_SIZE


class PresentationHandler:
    _presentation: Presentation
    _generator_handler: GenerationHandler
    _organizer: Organizer

    def __init__(self):
        self._presentation = Presentation()
        self._generator_handler = GenerationHandler()
        self._organizer = Organizer()

    @property
    def presentation(self):
        return self._presentation

    def reset(self):
        self._presentation = Presentation()

    def create_presentation(self, topic: Topic
                            , generators_names: list[str]
                            , params: dict[str, dict[str, object]]
                            , slides_number: int = -1) -> bool:
        # setting title
        try:
            self.presentation.title = topic.title

            self._generator_handler.generate_content(self.presentation, topic,
                                                     params, generators_names)

            logging.debug("keypoints generated successfully")
            logging.debug(self.presentation.all_keypoints)

            self._organizer.organize(self.presentation, topic, slides_number)
            logging.debug("presentation organized successfully")
            logging.debug(self.presentation.slides)

            return True
        except Exception as e:
            logging.error("Generation Failed")
            logging.exception(e)
            return False

    def export_presentation(self, path: str = RESULTS_DIR
                            , template: TEMPLATE = TEMPLATE.TEMPLATE_1):
        # fixme: this function is getting more complicated
        try:
            pr = pptx.Presentation(template.value)
            # adding title slide
            title_slide = pr.slides[0]
            title_slide.shapes.title.text = self.presentation.title
            # adding rest of slides
            for slide in self.presentation.slides:
                slide_layout = pr.slide_layouts[slide.layout.value]
                m_slide = pr.slides.add_slide(slide_layout)
                m_slide.shapes.title.text = slide.title
                # choosing the right placeholder for bullet points
                if slide.layout == LAYOUT.TITLE_AND_CONTENT:
                    holder_index = 1
                else:
                    holder_index = 2
                bullet_point_box = m_slide.shapes.placeholders[holder_index]

                bullet_points_text = [str(k.data) for k in slide.keypoints]
                bullet_point_box.text = "\n".join(bullet_points_text)
                # setting font size which is necessay for counting the number
                # of lines the text takes.
                for p in bullet_point_box.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(DEFAULT_BULLET_POINT_FONT_SIZE)
                # adding images if existed
                if slide.layout == LAYOUT.PICTURE_CONTENT_WITH_CAPTION:
                    image_box = m_slide.placeholders[CONTENT_PLACEHOLDER_IDX]
                    replace_with_image(str(slide.content.data)
                                       , image_box, m_slide)

            conclusion_slide_layout = pr.slide_layouts[LAYOUT.TITLE.value]
            conclusion_slide = pr.slides.add_slide(conclusion_slide_layout)
            conclusion_slide.shapes.title.text = "Conclusion"

            save_path = os.path.join(path, self.presentation.title + ".pptx")
            pr.save(save_path)

            logging.debug("Presentation exported successfully")
        except Exception as e:
            logging.error("Exporting FAILED")
            logging.exception(e)

    def get_presentation(self):
        return copy.deepcopy(self.presentation)
