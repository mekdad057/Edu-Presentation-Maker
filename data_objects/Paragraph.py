class Paragraph:
    title: str
    raw_data: str
    processed_data: str

    def __init__(self, title: str = "", raw: str = ""):
        self.title = title
        self.raw_data = raw
        self.processed_data = ""
