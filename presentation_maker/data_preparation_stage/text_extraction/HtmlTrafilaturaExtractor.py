import trafilatura

from presentation_maker.data_objects import Document, Paragraph
from presentation_maker.data_preparation_stage.text_extraction.Extractor import \
    Extractor


class HtmlTrafilaturaExtractor(Extractor):
    def __init__(self):
        super().__init__()

    def get_relevant_text(self, path: str) -> str:
        data = ""
        with open(path, 'rb') as f:
            data = f.read()

        extracted_content = trafilatura.bare_extraction(data,
                                                        include_formatting=True,
                                                        )
        return extracted_content['text']

    def get_paragraphs(self, doc: Document, text: str):
        paragraph_min_size = 100  # in chars
        split_text = text.split('##')

        # cleaning text from any empty strings
        cleaned_text = [text for text in split_text if len(text) > 0]

        # merging any small splits of text
        good_text = []
        block = ""
        for text in cleaned_text:
            if len(block) < paragraph_min_size:
                block = block + text
            else:
                good_text.append(block)
                block = text

        if len(block) < paragraph_min_size:
            good_text[-1] += block
        else:
            good_text.append(block)

        # adding paragraphs to the document
        for st in good_text:
            p = Paragraph(st)
            doc.paragraphs.append(p)
