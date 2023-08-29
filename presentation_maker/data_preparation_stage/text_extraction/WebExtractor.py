import logging

from bs4 import BeautifulSoup, Tag

from presentation_maker.data_objects import Document, Paragraph
from presentation_maker.data_preparation_stage.text_extraction.Extractor \
    import Extractor
from presentation_maker.utils import download_to_working, split_text_to_sentences, \
    divide_to_subarrays


class WebExtractor(Extractor):

    IMAGE_TAG: str
    MAX_SIZE_LIMIT: int
    NAME_DELIMITERS: str

    def __init__(self):
        super().__init__()
        self.NAME_DELIMITERS = "-|"
        self.IMAGE_VALID_SIZE = 30000
        self.IMAGE_TAG = "img"
        self.MAX_SIZE_LIMIT = 10

    def get_relevant_text(self, path: str) -> str:
        try:
            with open(path, 'rb') as f:
                data = f.read()
        except Exception as e:
            logging.debug("Couldn't read file in Extractor.")
            raise e

        from readability import Document

        doc = Document(data)
        content_html = doc.summary(html_partial=True)

        return content_html

    def get_paragraphs(self, doc: Document, text: str):
        # find text dense tag
        dense_tag = self._get_dense_tag(text)

        # get images with text,
        block = {"level": 1, "title": doc.name.split(".")[0], "text": ""
                 , "contents_paths": [], "is_structured": False}
        blocks = []
        dense_tags = BeautifulSoup(text, parser="lxml").find_all(
            lambda t: self._is_dense_tag(dense_tag, t)
                        or t.name == self.IMAGE_TAG)

        for tag in dense_tags:
            if tag.name == self.IMAGE_TAG:
                extracted = self.extract_content(tag)
                if extracted is not None:
                    block["contents_paths"].append(extracted)
                    if block["text"] != "":
                        blocks.append(block)
                        block = {"level": 1, "title": doc.name.split(".")[0]
                                 , "text": ""
                                 , "contents_paths": []
                                 , "is_structured": False}
            else:
                block["text"] += tag.get_text()
        if block["text"] != "":
            blocks.append(block)

        # break large blocks
        blocks = self._divide_large_blocks(blocks)

        # insert paragraphs
        doc.paragraphs = [Paragraph(block["title"]
                                    , block["text"]
                                    , block["contents_paths"]
                                    , block["is_structured"])
                          for block in blocks]

    def _get_dense_tag(self, text):
        main_content = BeautifulSoup(text, parser="lxml").find("html").find("body").find("div")
        text_tags = {}
        for f_tag in main_content.contents:
            if isinstance(f_tag, Tag):  # is it a tag ? YES
                for tag in f_tag.find_all([]):
                    key_name = "name:" + tag.name
                    text_tags[key_name] = text_tags.get(key_name, 0) + len(
                        tag.get_text())
                    if tag.has_attr("class"):
                        key_class = "class:" + " ".join(tag["class"])
                        text_tags[key_class] = text_tags.get(key_class, 0) \
                                               + len(tag.get_text())
        sorted_text_tags = dict(
            sorted(text_tags.items(), key=lambda x: x[1], reverse=True))
        result = next(iter(sorted_text_tags), None)
        logging.info(f"type of dense tag: {type(result)}")
        return result

    def _is_dense_tag(self, dense_tag, tag):
        dense_tag_type = dense_tag.split(":")[0]
        dense_tag_value = dense_tag.split(":")[1]
        if dense_tag.split(":")[0] == "name":
            return dense_tag_value == tag.name
        else:
            return dense_tag_value == (tag["class"]
                                       if tag.has_attr("class") else "None"
                                       )

    def extract_content(self, tag) -> str:
        """
        download content used in the wikipedia page, usually photos :param
        tag: reference to that tag contains the content usually <img>
        :return: path to the content downloaded in the working folder or None
        if the content is invalid
        """
        width = tag.get("width")
        height = tag.get("height")
        if width is None and height is None:
            return None
        width = float(width or height)
        height = float(height or width)
        if width * height <= self.IMAGE_VALID_SIZE:
            logging.debug("image too small %s" % str(width * height))
            return None

        url = tag.get("src")
        if "http" not in url:
            url = "https:" + url

        # this line will raise exception if you have problems with your internet
        # connection, the exception is handled in top calling class.
        path = download_to_working(url)
        return path

    def _divide_large_blocks(self, blocks):
        """
        divide blocks of text that exceed in the number of sentences
         a maximum limit MAX_SIZE_LIMIT
        :param blocks:
        :return:
        """
        new_blocks = []
        for block in blocks:
            block_sentences = split_text_to_sentences(block["text"])
            if len(block_sentences) > self.MAX_SIZE_LIMIT:
                number_of_new_blocks = len(block_sentences)\
                                     // self.MAX_SIZE_LIMIT + 1
                size_of_new_blocks = len(block_sentences)//number_of_new_blocks
                sentences_arrays = divide_to_subarrays(block_sentences
                                                       , size_of_new_blocks)
                for sentences in sentences_arrays:
                    new_block = {"level": block["level"], "title": block["title"]
                                 , "text": ".".join(sentences)
                                 , "contents_paths": block["contents_paths"]
                                 , "is_structured": block["is_structured"]}
                    new_blocks.append(new_block)
            else:
                new_blocks.append(block)
        return new_blocks

    def get_doc_name(self, work_path):
        try:
            with open(work_path, 'rb') as f:
                data = f.read()
        except Exception as e:
            logging.debug("Couldn't read file in Extractor.")
            raise e

        # get title tag from html
        title = BeautifulSoup(data, "lxml").find("title")
        name = title.get_text()
        for delimiter in self.NAME_DELIMITERS:
            name += delimiter
            name = name.split(delimiter)[0]

        return name
