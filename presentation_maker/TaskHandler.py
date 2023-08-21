from presentation_maker.data_preparation_stage import TopicHandler
from presentation_maker.presentation_genrating_stage import PresentationHandler


class TaskHandler:

    def __int__(self):
        self._topic_handler = TopicHandler("output")
        self._presentation_handler = PresentationHandler()

    def create_presentation(self, title: str
                            , paths: list[str]
                            , output_dir: str):
        self._topic_handler.reset(title)
        self._topic_handler.add_sources(paths)
        topic = self._topic_handler.topic

        self._presentation_handler.create_presentation(topic
                                                       , ["bart-large-cnn"]
                                                       , {"bart-large-cnn": {}})

        self._presentation_handler.export_presentation(output_dir)
    