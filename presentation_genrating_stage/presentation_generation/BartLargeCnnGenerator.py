import logging

import requests
from alive_progress import alive_bar
from tqdm import tqdm

from data_objects import Topic, KeyPoint
from presentation_genrating_stage.presentation_generation.Generator \
    import Generator


class BartGenerator(Generator):
    API_TOKEN: str
    API_URL: str
    HEADERS: dict

    def __init__(self):
        super().__init__("bart-large-cnn")
        self._INITIAL_PARAMS_VALUES = {"max_length": 90, "min_length": 30,
                                       "do_sample": False}
        self._current_params_values = {}
        self.API_TOKEN = "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"
        self.API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        self.HEADERS = {"Authorization": f"Bearer {self.API_TOKEN}"}

    def get_output(self, topic: Topic) \
            -> object:
        logging.debug(f"the summarizer used is bart-large-cnn")
        res = []
        # fixme: keypoints from different documents can't be distinguished
        #  in the result
        for doc in tqdm(topic.documents, desc="processing documents"):
            for p in tqdm(doc.paragraphs, desc="processing paragraphs", leave=False):
                # using api to summarize text
                input_text = p.processed_data

                request = {"inputs": input_text,
                           "parameters": {
                               "max_length": self.current_params_values[
                                   "max_length"],
                               "min_length": self.current_params_values[
                                   "min_length"],
                               "do_sample": self.current_params_values[
                                   "do_sample"]
                               }
                           }

                response = requests.post(self.API_URL, headers=self.HEADERS
                                         , json=request)

                if response.status_code == 200:
                    response_json = response.json()
                    # reading response
                    logging.info(response_json)
                    summary = response_json[0]["summary_text"]

                    # adding keypoints
                    p_keypoints = []
                    keypoint = KeyPoint(str(summary), p)
                    p_keypoints.append(keypoint)

                    res.append(p_keypoints)
                else:
                    logging.debug(
                        f"Failed to retrieve the URL due to the status code: "
                        f"{response.status_code}")
        return res
