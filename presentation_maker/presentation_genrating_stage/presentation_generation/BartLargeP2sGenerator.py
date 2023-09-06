import logging

import requests

from presentation_maker.data_objects import KeyPoint
from presentation_maker.presentation_genrating_stage.presentation_generation.Generator\
    import Generator
from presentation_maker.presentation_genrating_stage.presentation_generation.KeyPointGenerator \
    import KeyPointGenerator
from presentation_maker.utils import split_text_to_sentences, Config


@Generator.register_generator("bart-large-paper-2-slides-summarizer")
class BartLargeP2sGenerator(KeyPointGenerator):
    def __init__(self):
        super().__init__("bart-large-p2s")
        self._INITIAL_PARAMS_VALUES = {"max_length": 130, "min_length": 30,
                                       "do_sample": False}
        self._current_params_values = {}
        self.__API_TOKEN = Config.get("BartLargeP2sGenerator")["API_TOKEN"]
        self.__API_URL = Config.get("BartLargeP2sGenerator")["API_URL"]
        self.__HEADERS = {"Authorization": f"Bearer {self.__API_TOKEN}"}

    def _handle_unstructured_paragraph(self, paragraph):
        # summarizing
        summary = self.__request_summary(paragraph.processed_data)

        # adding keypoints
        p_keypoints = []
        for sentence in split_text_to_sentences(summary):
            if sentence != "":
                keypoint = KeyPoint(sentence, paragraph)
                p_keypoints.append(keypoint)

        return p_keypoints

    def __request_summary(self, text: str) -> str:
        # using api to summarize text

        request = {"inputs": text,
                   "parameters": {
                       "max_length": self.current_params_values[
                           "max_length"],
                       "min_length": self.current_params_values[
                           "min_length"],
                       "do_sample": self.current_params_values[
                           "do_sample"]
                   }
                   }
        while True:
            try:
                response = requests.post(self.__API_URL, headers=self.__HEADERS
                                         , json=request)
                logging.debug("status code : " + response.status_code.__str__())
                if response.status_code == 200:
                    break
            except Exception as e:
                logging.exception(e)

        return response.json()[0]["summary_text"]
