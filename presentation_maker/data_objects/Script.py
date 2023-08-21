from presentation_maker.data_objects.Content import Content


class Script(Content):
    reference: str

    def __init__(self, text, path):
        super().__init__(text, path)

