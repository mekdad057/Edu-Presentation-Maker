import copy
import logging
import os.path

import pptx

from data_objects import Presentation, Topic
from presentation_genrating_stage.presentation_generation import \
    GenerationHandler, Organizer
from utils import RESULTS_DIR
from utils.Errors import NotFoundError


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

    def export_presentation(self, path: str = RESULTS_DIR):
        try:
            pr = pptx.Presentation()
            # adding title slide
            title_slide = pr.slides.add_slide(pr.slide_layouts[0])
            title_slide.shapes.title.text = self.presentation.title

            for slide in self.presentation.slides:
                slide_register = pr.slide_layouts[1]
                m_slide = pr.slides.add_slide(slide_register)
                m_slide.shapes.title.text = slide.title
                bullet_point_box = m_slide.shapes
                bullet_point_lvl1 = bullet_point_box.placeholders[1]

                bullet_points_text = [str(k.data) for k in slide.keypoints]
                bullet_point_lvl1.text = "\n".join(bullet_points_text)

            conclusion_slide = pr.slides.add_slide(pr.slide_layouts[0])
            conclusion_slide.shapes.title.text = "Conclusion"

            save_path = os.path.join(path, self.presentation.title+".pptx")
            pr.save(save_path)

            logging.debug("Presentation exported successfully")
        except Exception as e:
            logging.error("Exporting FAILED")
            logging.exception(e)

    def get_presentation(self):
        return copy.deepcopy(self.presentation)
