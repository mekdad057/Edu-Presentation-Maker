from abc import ABC


class Content(ABC):
    data: object
    reference: object

    def __init__(self, data: object, reference: object):
        self.data = data
        self.reference = reference
