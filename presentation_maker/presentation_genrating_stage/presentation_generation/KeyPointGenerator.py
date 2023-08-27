import logging
from abc import abstractmethod

from tqdm import tqdm

from presentation_maker.data_objects import KeyPoint, Topic
from presentation_maker.presentation_genrating_stage.presentation_generation.Generator\
    import Generator
from presentation_maker.utils import is_sentence_empty, clear_sentence


class KeyPointGenerator(Generator):

    def __init__(self, name: str = "keypoint_generator"):
        super().__init__(name)

    def get_output(self, topic: Topic) -> object:
        res = []
        # fixme: keypoints from different documents can't be distinguished
        #  in the result
        for doc in tqdm(topic.documents, desc="processing documents"
                        , position=0, leave=True):
            for p in tqdm(doc.paragraphs, desc="processing paragraphs",
                          position=0, leave=True):
                p_keypoints = []

                if p.is_structured:
                    p_keypoints = self._handle_structured_paragraph(p)
                else:
                    p_keypoints = self._handle_unstructured_paragraph(p)

                res.append(p_keypoints)
        return res

    def _handle_structured_paragraph(self, paragraph) -> list[KeyPoint]:
        if not paragraph.is_structured:
            logging.warning("passing unstructured paragraphs to handle "
                            "as structured")
            return []

        result = []
        level_counter = 0
        keypoint_string = ""
        for char_ in paragraph.raw_data:
            if char_ == "#":
                if not is_sentence_empty(keypoint_string):
                    result.append(KeyPoint(clear_sentence(keypoint_string)
                                           , paragraph
                                           , level_counter))
                    level_counter = 0
                    keypoint_string = ""
                level_counter += 1
            else:
                keypoint_string += char_
        if not is_sentence_empty(keypoint_string):
            result.append(KeyPoint(clear_sentence(keypoint_string)
                                   , paragraph
                                   , level_counter))
        return result

    @abstractmethod
    def _handle_unstructured_paragraph(self, paragraph):
        pass

