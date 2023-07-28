import logging

from bs4 import BeautifulSoup

from data_objects import Document, Paragraph
from data_preparation_stage.data_extraction.DataSourceExtractor \
    import DataSourceExtractor
from utils import divide_to_subarrays
from utils.Errors import NotFoundError


class WikipediaExtractor(DataSourceExtractor):
    MAX_LIMIT: int
    MIN_LIMIT: int
    HEADINGS_TAGS: list[str]
    TEXT_TAGS: list[str]
    IGNORE: list[str]

    def __init__(self):
        super().__init__()
        self.HEADINGS_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6"]
        self.TEXT_TAGS = ["p"]  # fixme:  what about <ul> and <ol> tags?
        self.IGNORE = ["See also", "References", "Further reading", "Honors"
            , "Notes", "Sources", "External links"]
        self.MAX_LIMIT = 22
        self.MIN_LIMIT = 7

    def get_text(self, path: str) -> str:
        try:
            with open(path, 'rb') as f:
                data = f.read()
        except Exception as e:
            logging.debug("Couldn't read file in Extractor.")
            raise e

        soup = BeautifulSoup(data, 'html.parser')
        # the element of the page that contain all relevant text
        ob = soup.find(id="bodyContent")

        if ob is None:
            raise NotFoundError("Text Content", "bodyContent")

        # replacing all links with the text inside of them.
        for tag in ob.find_all("a"):
            tag.replace_with(tag.get_text())
        return ob.__unicode__()  # to return only the text without a reference
        # on the whole html tree

    def divide_paragraphs(self, doc: Document, text: str):
        """
        :param doc: the document which the paragraphs will be added to.
        :param text: the html tag that contains all the relevant text.
        :return: None
        """
        # blocks is a list of dictionaries that hold three values:
        #  level: the level of heading that has the text.
        #  title: the heading
        #  text: the actual text content directly under the heading.
        # 1- divide text to blocks
        blocks = self.divide_text_to_heading_blocks(text)
        # 2- divide long blocks
        blocks = self.divide_long_blocks(blocks)
        # 3- merge small blocks if possible or remove them
        blocks = self.merge_small_blocks(blocks)
        # 4- make paragraphs
        doc.paragraphs = [Paragraph(block["title"], block["text"])
                          for block in blocks]

    def divide_text_to_heading_blocks(self, text: str) -> list[dict]:
        soup = BeautifulSoup(text, 'html.parser')

        elements = soup.find_all(self.HEADINGS_TAGS + self.TEXT_TAGS)

        blocks = []
        # getting the introduction block (p tags directly under h1 heading).
        block = {"level": 1, "title": "Introduction", "text": ""}
        stop = 0  # to save where the first h2 heading starts
        for p in elements:
            if p.name not in self.TEXT_TAGS:
                stop = elements.index(p)
                break
            else:
                block["text"] += p.get_text()

        blocks.append(block)

        # getting the rest of the blocks
        # which are constructed like this 'h2, p, p, h3, p ,h3, p ...'
        # and elements array looks like this: [h2,p,p,...,h3,p,p,...,h2,p,p,...]
        block = {"level": -1, "title": "", "text": ""}
        for i in range(stop, len(elements)):
            if elements[i].name in self.HEADINGS_TAGS:
                if block["text"] != "":
                    blocks.append(block)
                    block = {"level": -1, "title": "", "text": ""}

                if elements[i].get_text(strip=True) not in self.IGNORE \
                        and elements[i].get_text(strip=True) not in \
                        [text + "[edit]" for text in self.IGNORE]:
                    block["title"] = elements[i].get_text(strip=True).replace(
                        "[edit]", "")
                    block["level"] = int(elements[i].name[-1])  # ex:the 3 in h3
                else:
                    block["title"] = ""
            else:
                block["text"] += elements[i].get_text()
        blocks.append(block)  # appending the last heading.
        return blocks

    def divide_long_blocks(self, blocks: list[dict]) -> list[dict]:
        res = []
        for b in blocks:
            b_sentences = b["text"].split(".")
            if len(b_sentences) > self.MAX_LIMIT:
                subs = divide_to_subarrays(b_sentences, self.MAX_LIMIT)

                # adding them as blocks
                for sub in subs:
                    block = {"level": b["level"], "title": b["title"]
                                , "text": ".".join(sub[1:])}

                    res.append(block)
            else:
                res.append(b)
        return res

    def merge_small_blocks(self, blocks: list[dict]) -> list[dict]:
        res = []
        index = -1
        for b in blocks:
            index += 1
            b_lvl = b["level"]
            b_sentences = b["text"].split(".")
            if len(b_sentences) < self.MIN_LIMIT and b_lvl != 1:
                # find children and merge with them.
                for i in range(index + 1, len(blocks)):
                    # check if blocks[i] is a child
                    cur_block_lvl = blocks[i]["level"]
                    if cur_block_lvl - 1 == b_lvl:
                        blocks[i]["text"] = b["text"] + blocks[i]["text"]
                        blocks[i]["title"] = b["title"] + ": " \
                                             + blocks[i]["title"]
                        blocks[i]["level"] = b["level"]
                    # if there are no more children
                    elif cur_block_lvl <= b_lvl:
                        break
                # remove b by not adding it to res
            else:
                res.append(b)
        return res
