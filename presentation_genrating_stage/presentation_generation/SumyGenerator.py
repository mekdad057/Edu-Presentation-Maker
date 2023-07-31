import logging

from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer

from data_objects import Topic, KeyPoint
from presentation_genrating_stage.presentation_generation.Generator \
    import Generator
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer


class SumyGenerator(Generator):
    def __init__(self):
        super().__init__("sumy")
        self._INITIAL_PARAMS_VALUES = {"n_sentences": 2
            , "summarizer": "lsa"}
        self._current_params_values = {}

    def get_output(self, topic: Topic) \
            -> object:
        res = []
        # fixme: keypoints from different documents can't be distinguished
        #  in the result
        for doc in topic.documents:
            for p in doc.paragraphs:
                parser = PlaintextParser(p.processed_data
                                         , Tokenizer(doc.language))
                summarizer = self.get_summarizer(
                    self._current_params_values["summarizer"])

                logging.debug(f"the summarizer used is "
                              f"{self._current_params_values['summarizer']} "
                              f"in the object {str(summarizer)}")

                summary = summarizer(parser.document
                                     ,
                                     self._current_params_values["n_sentences"])

                p_keypoints = []
                for sentence in summary:
                    keypoint = KeyPoint(str(sentence), p)
                    p_keypoints.append(keypoint)

                res.append(p_keypoints)

        return res

    def get_summarizer(self, name):
        if name == "lexrank":
            return LexRankSummarizer()
        elif name == "luhn":
            return LuhnSummarizer()
        elif name == "lsa":
            return LsaSummarizer()
        elif name == "textrank":
            return TextRankSummarizer()
        elif name == "kl-sum":
            return KLSummarizer()
        elif name == "sumbasic":
            return SumBasicSummarizer()
