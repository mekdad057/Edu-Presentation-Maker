class Paragraph:
    raw_data: str
    processed_data: str

    def __init__(self, raw: str = ""):
        self.raw_data = raw
        self.processed_data = ""
