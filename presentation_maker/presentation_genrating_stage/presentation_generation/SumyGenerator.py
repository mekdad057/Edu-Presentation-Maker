import logging

from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer

from presentation_maker.data_objects import KeyPoint
from presentation_maker.presentation_genrating_stage.presentation_generation.Generator\
    import Generator
from presentation_maker.presentation_genrating_stage.presentation_generation.KeyPointGenerator \
    import KeyPointGenerator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer


@Generator.register_generator("sumy")
class SumyGenerator(KeyPointGenerator):
    def __init__(self):
        super().__init__("sumy")
        self._INITIAL_PARAMS_VALUES = {"n_sentences": 2
            , "summarizer": "lsa"}
        self._current_params_values = {}

    def _handle_unstructured_paragraph(self, paragraph):
        parser = PlaintextParser(paragraph.processed_data
                                 , Tokenizer("english"))
        summarizer = self.__get_summarizer(
            self._current_params_values["summarizer"])

        summary = summarizer(parser.document,
                             self._current_params_values["n_sentences"])
        p_keypoints = []
        for sentence in summary:
            keypoint = KeyPoint(str(sentence), paragraph)
            p_keypoints.append(keypoint)
        return p_keypoints

    def __get_summarizer(self, name):
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
