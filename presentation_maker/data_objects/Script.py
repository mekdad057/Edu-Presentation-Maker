from presentation_maker.data_objects.Content import Content


class Script(Content):
    """
    explanation of an idea generated from the datasource.
    """
    reference: str

    def __init__(self, text, path):
        super().__init__(text, path)

