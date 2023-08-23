from presentation_maker.data_preparation_stage import TopicHandler
from presentation_maker.presentation_genrating_stage import PresentationHandler


class TaskHandler:
    _topic_handler: TopicHandler
    _presentation_handler: PresentationHandler

    def __init__(self):
        self._topic_handler = TopicHandler("output")
        self._presentation_handler = PresentationHandler()

    def create_presentation(self, title: str
                            , paths: list[str]
                            , output_dir: str
                            , generator_name: str = "bart-large-cnn"
                            , generator_params: dict[str, str] = {}):

        self._topic_handler.reset(title)

        self._topic_handler.add_sources(paths)
        topic = self._topic_handler.topic

        doc_names = [doc.name for doc in topic.documents]
        self._topic_handler.start_preprocessing(doc_names
                                                , ["citations_links_remover"
                                                   , "non_english_remover"
                                                   , "new_lines_remover"])

        self._presentation_handler.create_presentation(topic
                                                       , [generator_name]
                                                       , {generator_name: generator_params})

        self._presentation_handler.export_presentation(output_dir)
