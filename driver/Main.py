import os.path
import logging
import utils as u
from data_preparation_stage import TopicHandler
from presentation_genrating_stage import PresentationHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w"
                        , format="%(levelname)s - %(message)s"
                        , encoding="utf-8")

    t = TopicHandler("nuclear_tuning_lsa")  # FOR TESTING CHANGE HERE
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Computer.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Sorting_algorithm.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Muhammad_ibn_Musa_al-Khwarizmi.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Algebra.html"
    link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Nuclear_fusion.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Fyodor_Dostoevsky.html"
    t.add_source(link)

    for p in t.topic.documents[0].paragraphs:
        logging.debug(repr(p.raw_data))
    logging.debug("---")

    # FOR TESTING CHANGE HERE
    t.start_preprocessing(["Nuclear_fusion.html"]
                          , ["citations_links_remover"
                              , "html_tags_remover"
                              , "non_english_remover"
                              , "new_lines_remover"])
    for p in t.topic.documents[0].paragraphs:
        logging.debug(repr(p.processed_data))
    logging.debug("---")
    sumy_sums = ["lexrank", "luhn", "lsa", "textrank", "kl-sum", "sumbasic"]
    ph = PresentationHandler()
    ph.create_presentation(t.topic, ["sumy"],
                           {"sumy": {"summarizer": "lsa"}})

    ph.export_presentation()
