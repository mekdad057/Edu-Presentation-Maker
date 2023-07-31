from data_objects import Document
from data_preparation_stage.preprocessing.RepeatedWordsRemover\
    import RepeatedWordsRemover
from data_preparation_stage.preprocessing.DocumentProcessor\
    import DocumentProcessor
from data_preparation_stage.preprocessing.HtmlTagsRemover import HtmlTagsRemover
from data_preparation_stage.preprocessing.NewLinesRemover import NewLinesRemover
from data_preparation_stage.preprocessing.NonEnglishRemover import \
    NonEnglishRemover
from data_preparation_stage.preprocessing.Normalizer import Normalizer
from data_preparation_stage.preprocessing.PunctuationRemover import \
    PunctuationRemover
from data_preparation_stage.preprocessing.CitationsLinksRemover import \
    CitationsLinksRemover

from utils.Errors import NotFoundError


class PreprocessingHandler:

    def __init__(self):
        pass

    def process(self, documents: list[Document]
                    , processing_methods_names: list[str]):
        # finding all needed processors in order.
        processors = []
        for name in processing_methods_names:
            processors.append(self.get_processor(name))

        # preprocessing started
        for doc in documents:
            self.process_document(processors, doc)

    def process_document(self, processors: list[DocumentProcessor]
                         , document: Document):
        for processor in processors:
            processor.load_document(document)
            processor.process_document(document)

    def get_processor(self, name: str) -> DocumentProcessor:
        if name == "normalizer":
            return Normalizer()
        elif name == "punctuation_remover":
            return PunctuationRemover()
        elif name == "citations_links_remover":
            return CitationsLinksRemover()
        elif name == "non_english_remover":
            return NonEnglishRemover()
        elif name == "new_lines_remover":
            return NewLinesRemover()
        elif name == "html_tags_remover":
            return HtmlTagsRemover()
        elif name == "repeated_words_remover":
            return RepeatedWordsRemover()
        else:
            raise NotFoundError("processor", name)
