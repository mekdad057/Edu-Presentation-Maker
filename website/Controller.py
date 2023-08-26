class Controller:

    def __init__(self, model):
        self._model = model

    def create_presentation(self, title: str, paths: list[str]
                            , presentation_type: str = "simple"):
        return self._model.create_presentation(title, paths, presentation_type)
