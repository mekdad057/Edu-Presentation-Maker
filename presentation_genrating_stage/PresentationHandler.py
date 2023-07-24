import copy
import logging

from data_objects import Presentation, Topic
from presentation_genrating_stage.presentation_generation import \
    GenerationHandler, Organizer, Generator


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
                            , slides_number: int) -> bool:
        # setting title
        try:
            self.presentation.title = topic.title

            self._generator_handler.generate_content(self.presentation, topic
                                                     , generators_names)

            # self._organizer.organize(self.presentation, topic, slides_number)
            return True
        except Exception as e:
            logging.error("Generation Failed")
            logging.error(e)
            return False
    def export_presentation(self, path: str):
        pass

    def get_presentation(self):
        return copy.deepcopy(self.presentation)

