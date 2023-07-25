import logging

from data_objects import Content, Topic, KeyPoint
from presentation_genrating_stage.presentation_generation.Generator \
    import Generator
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


class SumyGenerator(Generator):
    def __init__(self):
        super().__init__("sumy")
        self._INITIAL_PARAMS_VALUES = {"n_sentences": 2}
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
                summarizer = LexRankSummarizer()
                summary = summarizer(parser.document
                                     , self._current_params_values["n_sentences"])

                p_keypoints = []
                for sentence in summary:
                    keypoint = KeyPoint(str(sentence), p)
                    p_keypoints.append(keypoint)

                res.append(p_keypoints)

        return res
