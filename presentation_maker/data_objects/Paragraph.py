
class Paragraph:
    """
    a coherent piece of text taken a data source
    """
    title: str
    raw_data: str
    processed_data: str
    contents_paths: list[str]
    is_structured: bool

    def __init__(self, title: str = "", raw: str = ""
                 , contents: list[str] = None, is_structured: bool = False):
        """

        :param title: title of the slide
        :param raw: text as it is from the datasource
        :param contents: paths to the contents inside the working directory
        :param is_structured: indicates if the Paragraph raw data are suitable
        to be included as they are in the presentation.
        """
        self.title = title
        self.raw_data = raw
        self.processed_data = ""
        self.contents_paths = list()
        if contents is not None:
            self.contents_paths = contents
        self.is_structured = is_structured
