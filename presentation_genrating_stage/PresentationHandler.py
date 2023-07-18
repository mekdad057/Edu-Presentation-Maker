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
                            , generators_names: list[Generator]
                            , slides_number: int):
        pass

    def export_presentation(self, path: str):
        pass
