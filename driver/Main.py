import logging
from data_preparation_stage import TopicHandler
from presentation_genrating_stage import PresentationHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w"
                        , format="%(levelname)s - %(message)s"
                        , encoding="utf-8")
    t = TopicHandler("Sorting Algorithm BBB")  # FOR TESTING CHANGE HERE
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Computer.html"
    link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Sorting_algorithm.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Muhammad_ibn_Musa_al-Khwarizmi.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Algebra.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Nuclear_fusion.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Fyodor_Dostoevsky.html"
    t.add_source(link)
    # fixme : bug, splitting sentences on . not a good idea
    #  for example: "O(n^2.7) run time." result is : "7) run time"
    for p in t.topic.documents[0].paragraphs:
        logging.debug(repr(p.raw_data))
    logging.debug("---")

    # FOR TESTING CHANGE HERE
    t.start_preprocessing(["Sorting_algorithm.html"]
                          , ["citations_links_remover"
                              , "non_english_remover"
                              , "new_lines_remover"])
    for p in t.topic.documents[0].paragraphs:
        logging.debug(repr(p.title))
        logging.debug(repr(p.processed_data))
    logging.debug("---")
    ph = PresentationHandler()
    ph.create_presentation(t.topic, ["bart-large-cnn"],
                           {"bart-large-cnn": {}})

    ph.export_presentation()

    # ph.reset()
    # t.topic.title += " p2s"
    # ph.create_presentation(t.topic, ["bart-large-paper-2-slides-summarizer"],
    #                        {"bart-large-paper-2-slides-summarizer": {}})
    # ph.export_presentation()
