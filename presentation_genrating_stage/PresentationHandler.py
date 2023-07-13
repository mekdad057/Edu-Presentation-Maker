from data_objects import Presentation, Topic
from presentation_genrating_stage.presentation_generation import \
    GenerationHandler, Organizer, Generator


class PresentationHandler:
    _presentation: Presentation
    _generator_handler: GenerationHandler
    _organizer: Organizer

    def create_presentation(self, topic: Topic
                            , generators_names: list[Generator]
                            , slides_number: int):
        pass

    def get_presentation(self):
        if self._presentation is None:
            self._presentation = Presentation()
        return self._presentation

    def export_presentation(self, path: str):
        pass
