import logging

from bs4 import BeautifulSoup
from tqdm import tqdm

from presentation_maker.data_objects import Document, Paragraph
from presentation_maker.data_preparation_stage.text_extraction.Extractor \
    import Extractor
from presentation_maker.utils import download_to_working, \
    split_text_to_sentences
from presentation_maker.utils.Errors import NotFoundError


class WikipediaExtractor(Extractor):

    MIN_LIMIT: int
    HEADINGS_TAGS: list[str]
    TEXT_TAGS: list[str]
    CONTENT_TAGS: list[str]
    IGNORE: list[str]
    IMAGE_CLASS: str
    IMAGE_TAG: str
    IMAGE_VALID_SIZE: int
    STRUCTURED_TEXT_TAGS: list[str]
    UNSTRUCTURED_TEXT_TAGS: list[str]

    def __init__(self):
        super().__init__()
        self.IMAGE_VALID_SIZE = 300
        self.HEADINGS_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6"]
        self.STRUCTURED_TEXT_TAGS = ["ul", "ol"]
        self.UNSTRUCTURED_TEXT_TAGS = ["p", "dd"]
        self.TEXT_TAGS = self.STRUCTURED_TEXT_TAGS + self.UNSTRUCTURED_TEXT_TAGS
        self.IGNORE = ["See also", "References", "Further reading", "Honors"
                       , "Notes", "Sources", "External links"]
        self.IMAGE_CLASS = "mw-file-element"
        self.IMAGE_TAG = "img"
        self.MIN_LIMIT = 2

    def get_relevant_text(self, path: str) -> str:
        try:
            with open(path, 'rb') as f:
                data = f.read()
        except Exception as e:
            logging.debug("Couldn't read file in Extractor.")
            raise e

        soup = BeautifulSoup(data, 'html.parser')
        # the element of the page that contain all relevant text
        ob = soup.find("div", class_="mw-parser-output")

        if ob is None:
            raise NotFoundError("Text Content", "bodyContent")

        return ob.__unicode__()  # to return only the text without a reference
        # on the whole html tree

    def get_paragraphs(self, doc: Document, text: str):
        """
        :param doc: the document which the paragraphs will be added to.
        :param text: the html tag that contains all the relevant text.
        :return: None
        """
        # blocks is a list of dictionaries that hold 4 values: level: the
        # level of heading that has the text. title: the heading text: the
        # actual text content directly under the heading. raw_contents: list
        # of content tags... like img, div, a,etc.
        # is_structured: boolean indicates if the structure of the paragraph
        # has to be preserved

        blocks = self.divide_text_to_heading_blocks(text)

        blocks = self.merge_small_blocks(blocks)

        doc.paragraphs = [Paragraph(block["title"]
                                    , block["text"]
                                    , block["contents_paths"]
                                    , block["is_structured"])
                          for block in blocks]

    def divide_text_to_heading_blocks(self, text: str) -> list[dict]:
        soup = BeautifulSoup(text, 'html.parser')

        elements = soup.find_all(self.TEXT_TAGS
                                 + self.HEADINGS_TAGS
                                 + [self.IMAGE_TAG])

        blocks = []
        # getting the introduction block (p tags directly under h1 heading).
        block = {"level": 1, "title": "Introduction", "text": ""
                 , "contents_paths": [], "is_structured": False}
        stop = 0  # to save where the first h2 heading starts
        pbar = tqdm(total=len(elements), desc="extracting elements:")
        for idx, tag in enumerate(elements):
            if tag.name not in self.TEXT_TAGS + [self.IMAGE_TAG]:
                stop = idx
                break
            else:
                self.extract_text(block, tag)
            pbar.update(1)

        blocks.append(block)

        # getting the rest of the blocks
        # which are constructed like this 'h2, p, p, h3, p ,h3, p ...'
        # and elements array looks like this: [h2,p,p,...,h3,p,p,...,h2,p,p,...]
        block = {"level": -1, "title": "", "text": "", "contents_paths": []
                 , "is_structured": False}
        for i in range(stop, len(elements)):
            if elements[i].name in self.HEADINGS_TAGS:
                if block["level"] != -1:
                    blocks.append(block)
                    block = {"level": -1, "title": "", "text": ""
                             , "contents_paths": [], "is_structured": False}

                if elements[i].get_text(strip=True) not in self.IGNORE \
                        and elements[i].get_text(strip=True) not in \
                        [text + "[edit]" for text in self.IGNORE]:
                    block["title"] = elements[i].get_text(strip=True).replace(
                        "[edit]", "")
                    block["level"] = int(elements[i].name[-1])  # ex:the 3 in h3
                else:
                    break
            else:
                self.extract_text(block, elements[i])
            pbar.update(1)
        blocks.append(block)  # appending the last heading.
        pbar.update(len(elements) - pbar.n)
        pbar.close()
        return blocks

    def merge_small_blocks(self, blocks: list[dict]) -> list[dict]:
        res = []
        index = -1
        for b in blocks:
            index += 1
            b_lvl = b["level"]
            b_sentences = split_text_to_sentences(b["text"])
            if len(b_sentences) < self.MIN_LIMIT and b_lvl != 1:
                # find children and merge with them.
                for i in range(index + 1, len(blocks)):
                    # check if blocks[i] is a child
                    cur_block_lvl = blocks[i]["level"]
                    if cur_block_lvl - 1 == b_lvl \
                            and not blocks[i]["is_structured"]:
                        blocks[i]["text"] = b["text"] + blocks[i]["text"]
                        blocks[i]["title"] = b["title"] + ": " \
                                             + blocks[i]["title"]
                        blocks[i]["level"] = b["level"]
                        blocks[i]["contents_paths"] = \
                            b["contents_paths"] + blocks[i]["contents_paths"]
                    # if there are no more children
                    elif cur_block_lvl <= b_lvl:
                        break
                    # fixing the level of sub-children
                    else:
                        blocks[i]["level"] -= 1
                # remove b by not adding it to res
            else:
                res.append(b)
        return res

    def extract_content(self, tag) -> str:
        """
        download content used in the wikipedia page, usually photos :param
        tag: reference to that tag contains the content usually <img>
        :return: path to the content downloaded in the working folder or None
        if the content is invalid
        """
        url = ""
        class_ = tag.get("class")
        # checking if the image is a valid image
        if class_ is None or class_[0] != self.IMAGE_CLASS:
            return None
        width = tag.get("width")
        height = tag.get("height")
        if width is None or height is None:
            return None
        width = float(width)
        height = float(height)
        if width*height <= self.IMAGE_VALID_SIZE:
            logging.debug("image too small %s" % str(width*height))
            return None

        url = tag.get("src")
        if "http" not in url:
            url = "https:" + url

        # this line will raise exception if you have problems with your internet
        # connection, the exception is handled in top calling class.
        path = download_to_working(url)
        return path

    def extract_text(self, block, element):
        if element.name == self.IMAGE_TAG:
            extracted = self.extract_content(element)
            if extracted is not None:
                block["contents_paths"].append(extracted)
        elif element.name in self.STRUCTURED_TEXT_TAGS:
            try:
                if len(split_text_to_sentences(block["text"])) <= self.MIN_LIMIT:
                    block["is_structured"] = True
                    block["text"] += "\n" + self.extract_list(element)
                else:
                    block["text"] += element.get_text()
            except Exception as e:
                logging.exception(e)
                block["text"] += element.get_text()
        else:
            block["text"] += element.get_text()

    def extract_list(self, element, level: int = 1) -> str:
        """
        extracts text from list tag while preserving the structure of the list,
        iterate over list items adding a level up for each list item to be
        explored, the [ul, ol] tags don't add levels because they're styling
        tags and don't contain text
        :param element: the list main tag
        :param level: the level of the list item.
        :return: extracted text that contains the structure of the list by using
         # character to represent the level of each list item
        """
        result = ""
        for list_element in element.contents:
            if list_element.name == "li":
                lists = list_element.find_all(self.STRUCTURED_TEXT_TAGS)
                for inner_list in lists:
                    inner_list.replace_with(self.extract_list(inner_list
                                                              , level + 1))
                result += "#"*level + list_element.get_text()
        return result

    def get_doc_name(self, work_path) -> str:
        return super().get_doc_name(work_path)
