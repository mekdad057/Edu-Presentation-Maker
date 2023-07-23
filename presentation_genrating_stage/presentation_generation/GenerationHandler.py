from data_objects import Presentation, Topic, KeyPoint
from presentation_genrating_stage.presentation_generation.Generator\
    import Generator
from presentation_genrating_stage.presentation_generation.SumyGenerator import \
    SumyGenerator


class GenerationHandler:
    language: str
    # first key is the name of the generator and the second key is the
    # parameter value
    INITIAL_GENERATOR_PARAMS_VALUES: dict[str, dict[str, object]]

    KEYPOINT_GENERATORS: list[str]
    SCRIPT_GENERATORS: list[str]

    def __init__(self, language: str = "all"):
        self.language = language
        self.SCRIPT_GENERATORS = []
        self.KEYPOINT_GENERATORS = ["Sumy"]
        self.INITIAL_GENERATOR_PARAMS_VALUES = {}

    def generate_content(self, presentation: Presentation, topic: Topic
                         , generators_names: list[str]):
        # validating the choice of generators
        if len(generators_names) > 2:
            raise ValueError("Only one keypoint and one script generators "
                             "are allowed")

        if not set(generators_names).issubset(
                set(self.SCRIPT_GENERATORS+self.KEYPOINT_GENERATORS)
        ):
            raise ValueError(f'''Not Valid Generators' names
            supported keypoint generators: {self.KEYPOINT_GENERATORS}
            supported script generators: {self.SCRIPT_GENERATORS}
            ''')

        # generating keypoints
        kp_generator = self.get_kp_generator(generators_names)
        self.generate_keypoints(presentation, topic, kp_generator)

    def generate_keypoints(self, presentation: Presentation, topic: Topic
                           , generator: Generator):
        res = generator.get_output(topic, {})

        for content in res:
            presentation.all_keypoints.append(KeyPoint(str(content.data)
                                                       , content.reference))

    def generate_script(self, presentation: Presentation, topic: Topic
                        , generator: Generator):
        pass

    def get_s_generator(self, name: str) -> Generator:
        pass

    def get_kp_generator(self, generators_names) -> Generator:
        for name in generators_names:
            if name == "Sumy":
                return SumyGenerator()
        return None