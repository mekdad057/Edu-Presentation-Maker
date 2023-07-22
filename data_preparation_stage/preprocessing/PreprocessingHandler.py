from data_objects import Topic, Document
from data_preparation_stage.preprocessing import DocumentProcessor
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
            for processor in processors:
                processor.process_document(doc)

    def process_document(self, processors: list[DocumentProcessor]
                         , document: Document):
        for processor in processors:
            processor.process_document(document)

    def get_processor(self, name: str) -> DocumentProcessor:
        if name == "normalizer":
            return Normalizer()
        elif name == "punctuation_remover":
            return PunctuationRemover()
        elif name == "citations_links_remover":
            return CitationsLinksRemover()
        else:
            raise NotFoundError(f"processor with name {name} not found")
