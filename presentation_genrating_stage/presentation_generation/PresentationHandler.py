from data_objects import Presentation, Topic
from presentation_genrating_stage.presentation_generation import Generator, \
    GeneratorHandler, Organizer


class PresentationHandler:
    _presentation: Presentation
    _generator_handler: GeneratorHandler
    _organizer: Organizer

    def create_presentation(self, topic: Topic
                            , generators_names: list[Generator]
                            , slides_number: int):
        pass

    def get_presentation(self):
        return self._presentation

    def export_presentation(self, path: str):
        pass

