from data_objects.Content import Content


class Paragraph:
    title: str
    raw_data: str
    processed_data: str
    contents_paths: list[str]

    def __init__(self, title: str = "", raw: str = ""
                 , contents: list[str] = None):
        self.title = title
        self.raw_data = raw
        self.processed_data = ""
        self.contents_paths = list()
        if contents is not None:
            self.contents_paths = contents
