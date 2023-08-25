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

    def __init__(self):
        pass

    def process(self, documents: list[Document]
                    , processing_methods_names: list[str]):
        # finding all needed processors in order.
        processors = []
        for name in processing_methods_names:
            processors.append(self.get_processor(name))

        # text_preprocessing started
        for doc in documents:
            self.process_document(processors, doc)

    def process_document(self, processors: list[Processor]
                         , document: Document):
        for processor in processors:
            processor.load_document(document)
            processor.process_document(document)

    def get_processor(self, name: str) -> Processor:
        if name == "normalizer":
            return Normalizer()
        elif name == "punctuation_remover":
            return PunctuationRemover()
        elif name == "citations_links_remover":
            return CitationsLinksRemover()
        elif name == "non_english_remover":
            return NonEnglishMathSafeRemover()
        elif name == "new_lines_remover":
            return NewLinesRemover()
        elif name == "html_tags_remover":
            return HtmlTagsRemover()
        elif name == "repeated_words_remover":
            return RepeatedWordsRemover()
        else:
            raise NotFoundError("processor", name)
