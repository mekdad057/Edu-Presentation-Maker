import copy
import logging
import os.path

import pptx

from data_objects import Presentation, Topic
from presentation_genrating_stage.presentation_generation import \
    GenerationHandler, Organizer, Generator
from utils import WORKING_DIR


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
            logging.error(e)
            return False

    def export_presentation(self, path: str = WORKING_DIR):
        pr = pptx.Presentation()

        for slide in self.presentation.slides:
            slide_register = pr.slide_layouts[1]
            m_slide = pr.slides.add_slide(slide_register)
            m_slide.shapes.title.text = slide.title
            bullet_point_box = m_slide.shapes
            bullet_point_lvl1 = bullet_point_box.placeholders[1]

            bullet_points_text = [str(k.data) for k in slide.keypoints]
            bullet_point_lvl1.text = "\n".join(bullet_points_text)

        pr.save(os.path.join(path, self.presentation.title+".pptx"))

        logging.debug("presentation exported successfully")


    def get_presentation(self):
        return copy.deepcopy(self.presentation)
