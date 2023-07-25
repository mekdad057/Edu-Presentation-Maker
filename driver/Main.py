import os.path
import logging
import utils as u
from data_preparation_stage import TopicHandler
from presentation_genrating_stage import PresentationHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w"
                        , format="%(levelname)s - %(message)s"
                        , encoding="utf-8")

    t = TopicHandler("writers")
    # link = "https://en.wikipedia.org/wiki/Nuclear_fusion"
    link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Nuclear_fusion.html"
    # link = "https://en.wikipedia.org/wiki/Fyodor_Dostoevsky"
    # link = "https://ar.wikipedia.org/wiki/%D8%A7%D9%84%D9%85%D9%84%D8%AD%D9" \
    #       "%85%D8%A9_%D8%A7%D9%84%D9%83%D8%A8%D8%B1%D9%89"
    t.add_source(link)

    for p in t.topic.documents[0].paragraphs:
        logging.debug(repr(p.raw_data))
    logging.debug("---")

    t.start_preprocessing(["Nuclear_fusion.html"]
                          , ["citations_links_remover"
                              , "non_english_remover"
                             , "new_lines_remover"])
    for p in t.topic.documents[0].paragraphs:
        logging.debug(repr(p.processed_data))
    logging.debug("---")

    ph = PresentationHandler()
    ph.create_presentation(t.topic, ["sumy"], {})








