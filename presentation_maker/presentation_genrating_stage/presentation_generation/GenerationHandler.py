from presentation_maker.data_objects import Presentation, Topic
from presentation_maker.presentation_genrating_stage.presentation_generation.BartLargeCnnGenerator import \
    BartLargeCnnGenerator
from presentation_maker.presentation_genrating_stage.presentation_generation.BartLargeP2sGenerator import \
    BartLargeP2sGenerator
from presentation_maker.presentation_genrating_stage.presentation_generation.Generator \
    import Generator
from presentation_maker.presentation_genrating_stage.presentation_generation.SumyGenerator import \
    SumyGenerator
from presentation_maker.utils.Errors import NotFoundError


class GenerationHandler:

    # params: first key is the name of the generator and the second key is the
    # parameter value
    def generate_content(self, presentation: Presentation, topic: Topic
                         , params: dict[str, dict[str, object]]
                         , generators_names: list[str]):
        # validating the choice of generators
        if len(generators_names) > 2:
            raise ValueError("Only one keypoint and one script generators "
                             "are allowed")
        # checking that if two generators were given then
        # they don't do the same thing.
        # n_kp_generators = 0  # number of keypoint generators given.
        # n_s_generators = 0  # number of script generators given.
        # for name in generators_names:
        #     if name in self.KEYPOINT_GENERATORS:
        #         n_kp_generators += 1
        #     if name in self.SCRIPT_GENERATORS:
        #         n_s_generators += 1
        # if n_kp_generators == 1 and n_s_generators == 1 \
        #         and n_s_generators+n_kp_generators == 2:
        #     raise ValueError(f'''Not Valid Generators' names
        #     supported keypoint generators: {self.KEYPOINT_GENERATORS}
        #     supported script generators: {self.SCRIPT_GENERATORS}
        #     ''')

        # generating keypoints
        kp_generator = self.__get_generator(generators_names, params)
        self.__generate_keypoints(presentation, topic, kp_generator)

    def __generate_keypoints(self, presentation: Presentation, topic: Topic
                             , generator: Generator):
        res = generator.get_output(topic)

        presentation.all_keypoints = res

    def __get_generator(self, generators_names
                        , params: dict[str, dict[str, object]]) -> Generator:
        generator = None
        for name in generators_names:
            generator_class = Generator.registry().get(name)
            if generator_class:
                generator = generator_class()

        generator.current_params_values = params.get(generator.NAME, {})
        return generator
