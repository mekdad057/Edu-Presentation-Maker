from presentation_maker.data_objects import Document
from presentation_maker.data_preparation_stage.text_preprocessing.RepeatedWordsRemover \
    import RepeatedWordsRemover
from presentation_maker.data_preparation_stage.text_preprocessing.Processor \
    import Processor
from presentation_maker.data_preparation_stage.text_preprocessing.HtmlTagsRemover\
    import HtmlTagsRemover
from presentation_maker.data_preparation_stage.text_preprocessing.NewLinesRemover\
    import NewLinesRemover
from presentation_maker.data_preparation_stage.text_preprocessing.NonEnglishMathSafeRemover\
    import NonEnglishMathSafeRemover
from presentation_maker.data_preparation_stage.text_preprocessing.Normalizer\
    import Normalizer
from presentation_maker.data_preparation_stage.text_preprocessing.PunctuationRemover\
    import \
    PunctuationRemover
from presentation_maker.data_preparation_stage.text_preprocessing.CitationsLinksRemover\
    import CitationsLinksRemover

from presentation_maker.utils.Errors import NotFoundError


class PreprocessingHandler:

    def process(self, documents: list[Document]
                    , processing_methods_names: list[str]):
        # finding all needed processors in order.
        processors = []
        for name in processing_methods_names:
            processors.append(self._get_processor(name))

        # text_preprocessing started
        for doc in documents:
            self._process_document(processors, doc)

    def _process_document(self, processors: list[Processor]
                          , document: Document):
        for processor in processors:
            processor.load_document(document)
            processor.process_document(document)
            processor.unload()

    def _get_processor(self, name: str) -> Processor:
        processor_class = Processor.registry().get(name)
        if processor_class:
            return processor_class()
        else:
            raise NotFoundError("processor", name)
