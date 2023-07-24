from bs4 import BeautifulSoup

from data_objects import Document, Paragraph
from data_preparation_stage.data_extraction.DataSourceExtractor \
    import DataSourceExtractor


class WikipediaExtractor(DataSourceExtractor):
    def __init__(self):
        super().__init__()

    def get_text(self, path: str) -> str:
        data = ""
        with open(path, 'rb') as f:
            data = f.read()

        soup = BeautifulSoup(data, 'html.parser')
        # the element of the page that contain all relevant text
        ob = soup.find(id="bodyContent")
        # replacing all links with the text inside of them.
        for tag in ob.find_all("a"):
            tag.replace_with(tag.get_text())

        return ob.__unicode__()  # to return only the text without a reference
        # on the whole html tree

    def divide_paragraphs(self, doc: Document, text: str):
        soup = BeautifulSoup(text, 'html.parser')

        elements = soup.find_all(["h2", "p"])

        # getting the introduction paragraph.
        block = "Introduction"
        for p in elements:
            if p.name != 'p':
                break
            else:
                block += p.get_text()
        paragraph = Paragraph(block)
        doc.paragraphs.append(paragraph)

        # getting the rest of the paragraphs
        # which are constructed like this 'h2, p, p ...'
        # and elements array looks like this: [h2,p,p,...,h2,p,p,...,h2,p,p,...]
        block = ""
        headings = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        ignore = ["See also[edit]", "References[edit]", "Further reading[edit]"]
        for i in range(len(elements)):
            if elements[i].name in headings or i == len(elements)-1:
                if block != "" and elements[i].name == 'h2':
                    paragraph = Paragraph(block)
                    doc.paragraphs.append(paragraph)

                if elements[i].get_text(strip=True) not in ignore:
                    block = elements[i].get_text(strip=True) + '\n'
                else:
                    block = ""
            else:
                block += elements[i].get_text()
