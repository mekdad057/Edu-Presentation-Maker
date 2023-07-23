from data_objects import Content, Topic, KeyPoint
from presentation_genrating_stage.presentation_generation.Generator \
    import Generator
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


class SumyGenerator(Generator):
    def __init__(self):
        super().__init__()
        self._Name = "Sumy"
        self._INITIAL_PARAMS_VALUES = {"percentage": 0.25}
        self._current_params_values = {}

    def get_output(self, topic: Topic, params: dict[str, object]) \
            -> list[Content]:
        res = list()
        per = params.get("percentage",
                         self._INITIAL_PARAMS_VALUES["percentage"])

        for doc in topic.documents:
            summary = ""
            for p in doc.paragraphs:
                # getting percentage from all sentences in a paragraph
                amount = int(per * len(p.processed_data.split('.')))
                parser = PlaintextParser.from_string(p.processed_data
                                                     , Tokenizer("english"))
                # getting summary of the paragraph
                summarizer = LexRankSummarizer()
                summary = summarizer(parser.document, amount)

            c = KeyPoint(summary, doc.path)
            res.append(c)

        return res
