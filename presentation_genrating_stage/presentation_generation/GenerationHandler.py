from data_objects import Presentation, Topic


class GenerationHandler:
    language: str
    # first key is the name of the generator and the second key is the
    # parameter value
    INITIAL_GENERATOR_PARAMS_VALUES: dict[str, dict[str, str]]

    KEYPOINT_GENERATORS: list[str]
    SCRIPT_GENERATORS: list[str]

    def generate_content(self, presentation: Presentation, topic: Topic
                         , generators_names: list[str]) -> Presentation:
        pass

    def generate_keypoints(self, presentation: Presentation, topic: Topic
                           , generators_name: str) -> Presentation:
        pass

    def generate_script(self, presentation: Presentation, topic: Topic
                        , generators_name: str) -> Presentation:
        pass
