from presentation_maker.data_objects.Paragraph import Paragraph
from presentation_maker.data_objects.Content import Content


class Image(Content):
    """
    Image used in the presentation
    """
    def __init__(self, data: object, reference: Paragraph):
        """
        :param data: path of the image in the working directory.
        :param reference: the slide that is inserted in.
        """
        super().__init__(data, reference)
