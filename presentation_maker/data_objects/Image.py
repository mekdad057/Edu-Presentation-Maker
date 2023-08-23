from presentation_maker.data_objects.Content import Content


class Image(Content):
    def __init__(self, data: object, reference: object):
        """
        :param data: path of the image in the working directory.
        :param reference: the slide that is inserted in.
        """
        super().__init__(data, reference)
