import logging

import requests

from presentation_maker.data_objects import KeyPoint
from presentation_maker.presentation_genrating_stage.presentation_generation.KeyPointGenerator \
    import KeyPointGenerator
from presentation_maker.utils import split_text_to_sentences


class BartLargeCnnGenerator(KeyPointGenerator):
    API_TOKEN: str
    API_URL: str
    HEADERS: dict

    def __init__(self):
        super().__init__("bart-large-cnn")
        self._INITIAL_PARAMS_VALUES = {"max_length": 130, "min_length": 30,
                                       "do_sample": False}
        self._current_params_values = {}
        self.API_TOKEN = "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"
        self.API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        self.HEADERS = {"Authorization": f"Bearer {self.API_TOKEN}"}

    def _handle_unstructured_paragraph(self, paragraph):
        # summarizing
        summary = self.request_summary(paragraph.processed_data)

        # adding keypoints
        p_keypoints = []
        for sentence in split_text_to_sentences(summary):
            if sentence != "":
                keypoint = KeyPoint(sentence, paragraph)
                p_keypoints.append(keypoint)

        return p_keypoints

    def request_summary(self, text: str) -> str:
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
                response = requests.post(self.API_URL, headers=self.HEADERS
                                         , json=request)
                logging.debug("status code : " + response.status_code.__str__())
                if response.status_code == 200:
                    break
            except Exception as e:
                logging.exception(e)

        return response.json()[0]["summary_text"]
