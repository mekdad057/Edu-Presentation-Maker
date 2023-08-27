from abc import ABC


class Content(ABC):
    """
    any type of content that can be generated or extracted.
    """
    data: object
    reference: object

    def __init__(self, data: object, reference: object):
        self.data = data
        self.reference = reference
