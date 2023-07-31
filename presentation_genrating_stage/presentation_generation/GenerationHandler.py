from data_objects import Presentation, Topic, KeyPoint
from presentation_genrating_stage.presentation_generation.BartLargeCnnGenerator import \
    BartGenerator
from presentation_genrating_stage.presentation_generation.Generator \
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

    def __init__(self, language: str = "english"):
        self.language = language
        self.SCRIPT_GENERATORS = []
        self.KEYPOINT_GENERATORS = ["sumy", "bart-large-cnn"]
        self.INITIAL_GENERATOR_PARAMS_VALUES = {}

    def generate_content(self, presentation: Presentation, topic: Topic
                         , params: dict[str, dict[str, object]]
                         , generators_names: list[str]):
        # todo : improve validation for generators (HERE)
        # validating the choice of generators
        if len(generators_names) > 2:
            raise ValueError("Only one keypoint and one script generators "
                             "are allowed")
        # checking that if two generators were given then
        # they don't do the same thing.
        n_kp_generators = 0  # number of keypoint generators given.
        n_s_generators = 0  # number of script generators given.
        for name in generators_names:
            if name in self.KEYPOINT_GENERATORS:
                n_kp_generators += 1
            if name in self.SCRIPT_GENERATORS:
                n_s_generators += 1
        if n_kp_generators == 1 and n_s_generators == 1 \
                and n_s_generators+n_kp_generators == 2:
            raise ValueError(f'''Not Valid Generators' names
            supported keypoint generators: {self.KEYPOINT_GENERATORS}
            supported script generators: {self.SCRIPT_GENERATORS}
            ''')

        # generating keypoints
        kp_generator = self.get_kp_generator(generators_names, params)
        self.generate_keypoints(presentation, topic, kp_generator)

    def generate_keypoints(self, presentation: Presentation, topic: Topic
                           , generator: Generator):
        res = generator.get_output(topic)

        presentation.all_keypoints = res

    def generate_script(self, presentation: Presentation, topic: Topic
                        , generator: Generator):
        pass

    def get_s_generator(self, name: str) -> Generator:
        pass

    def get_kp_generator(self, generators_names
                         , params: dict[str, dict[str, object]]) -> Generator:
        generator = None
        for name in generators_names:
            if name == "sumy":
                generator = SumyGenerator()
            elif name == "bart-large-cnn":
                generator = BartGenerator()
        generator.current_params_values = params.get(generator.NAME, {})
        return generator
