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
        self.MAX_LIMIT = 20
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
        # 1- divide text to blocks
        blocks = self.divide_text_to_heading_blocks(text)
        # 2- divide long blocks
        blocks = self.divide_long_blocks(blocks)
        # 3- merge small blocks if possible or remove them
        blocks = self.merge_small_blocks(blocks)
        # 4- make paragraphs
        doc.paragraphs = [Paragraph(block.split("<")[0], block)
                          for block in blocks]

    def divide_text_to_heading_blocks(self, text: str) -> list[str]:
        soup = BeautifulSoup(text, 'html.parser')

        elements = soup.find_all(self.HEADINGS_TAGS + self.TEXT_TAGS)

        blocks = []
        # todo : write a block class that has the "level" attribute in it
        #  instead of inserting words to the original text.
        # getting the introduction block (p tags directly under h1 heading).
        block = "Introduction<h1>\n"
        stop = 0  # to save where the first h2 heading starts
        for p in elements:
            if p.name not in self.TEXT_TAGS:
                stop = elements.index(p)
                break
            else:
                block += p.get_text()

        blocks.append(block)

        # getting the rest of the blocks
        # which are constructed like this 'h2, p, p, h3, p ,h3, p ...'
        # and elements array looks like this: [h2,p,p,...,h3,p,p,...,h2,p,p,...]
        block = ""
        for i in range(stop, len(elements)):
            if elements[i].name in self.HEADINGS_TAGS or i == len(elements) - 1:
                if block != "":
                    blocks.append(block)

                if elements[i].get_text(strip=True) not in self.IGNORE \
                        and elements[i].get_text(strip=True) not in \
                        [text + "[edit]" for text in self.IGNORE]:
                    # first sentence in block represent the heading
                    # for example: block = "heading_text|#3\n"
                    block = elements[i].get_text(strip=True) + \
                            f"<{elements[i].name}>" + "\n"
                    block = block.replace("[edit]", "")
                else:
                    block = ""
            else:
                block += elements[i].get_text()
        return blocks

    def divide_long_blocks(self, blocks: list[str]) -> list[str]:
        res = []
        for b in blocks:
            b_sentences = b.split(".")
            if len(b_sentences) > self.MAX_LIMIT:
                subs = divide_to_subarrays(b_sentences, self.MAX_LIMIT)
                # adding heading for each subarray of sentences to ensure that
                # all of them belong to the same topic
                heading_text = b.split("\n")[0]
                for i in range(1, len(subs)):  # starts from 1 because 0 has a heading
                    subs[i] = [heading_text+'\n'] + subs[i]
                # adding them as blocks
                for sub in subs:
                    res.append(".".join(sub))
            else:
                res.append(b)
        return res

    def merge_small_blocks(self, blocks: list[str]) -> list[str]:
        res = []
        index = -1
        for b in blocks:
            index += 1
            b_lvl = int(b.split(">")[0][-1])  # the digit in "<h3>"
            b_sentences = b.split(".")
            if len(b_sentences) < self.MIN_LIMIT and b_lvl != 1:
                # find children and merge with them.
                for i in range(index + 1, len(blocks)):
                    # check if blocks[i] is a child
                    cur_block_lvl = int(blocks[i].split(">")[0][-1])
                    if cur_block_lvl - 1 == b_lvl:
                        blocks[i] = b + blocks[i]
                    # if there are no more children
                    if cur_block_lvl <= b_lvl:
                        break
                # remove b by not adding it to res
            else:
                res.append(b)
        return res
