class Controller:

    def __init__(self, model):
        self._model = model

    def create_presentation(self, title: str, paths: list[str]):
        return self._model.create_presentation(title, paths)
