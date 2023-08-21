
class Paragraph:
    title: str
    raw_data: str
    processed_data: str
    contents_paths: list[str]
    is_structured: bool

    def __init__(self, title: str = "", raw: str = ""
                 , contents: list[str] = None, is_structured: bool = False):
        self.title = title
        self.raw_data = raw
        self.processed_data = ""
        self.contents_paths = list()
        if contents is not None:
            self.contents_paths = contents
        self.is_structured = is_structured
