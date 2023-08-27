import logging
from presentation_maker.data_preparation_stage import TopicHandler
from presentation_maker.presentation_genrating_stage import PresentationHandler

if __name__ == "__main__":
    # todo: add logger instead of using logging to avoid logging messages
    #  from inside packages.
    # todo : do testing on wiki pages.!!!!!!!!!!!!!!!!!!
    logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w"
                        , format="%(levelname)s - %(message)s"
                        , encoding="utf-8")
    t = TopicHandler("Alan Turing")  # FOR TESTING CHANGE HERE

    # link = "https://en.wikibooks.org/wiki/Artificial_Intelligence_for_Computational_Sustainability%3A_A_Lab_Companion%2FMachine_Learning_for_Prediction"
    # link = "https://www.aps.org/programs/outreach/physicsquest/past/falling-physics.cfm#:~:text=When%20something%20falls%2C%20it%20falls,is%20a%20type%20of%20acceleration."
    # link = "https://www.techtarget.com/whatis/definition/transistor#:~:text=A%20transistor%20is%20a%20miniature,which%20can%20carry%20a%20current."
    # link = "https://www.ibm.com/topics/artificial-intelligence"
    link = "https://www.britannica.com/technology/artificial-intelligence/Alan-Turing-and-the-beginning-of-AI"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Computer.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Sorting_algorithm.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Muhammad_ibn_Musa_al-Khwarizmi.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Algebra.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Nuclear_fusion.html"
    # link = r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\working\Fyodor_Dostoevsky.html"
    t.add_source(link)
    doc_name = t.topic.documents[0].name
    for p in t.topic.documents[0].paragraphs:
        logging.debug(repr(p.raw_data))
    logging.debug("---")

    # FOR TESTING CHANGE HERE
    t.start_preprocessing([doc_name]
                          , ["citations_links_remover"
                              , "non_english_remover"
                              , "new_lines_remover"])
    for p in t.topic.documents[0].paragraphs:
        logging.debug(repr(p.title))
        logging.debug(p.is_structured)
        logging.debug(repr(p.processed_data))
    logging.debug("---")
    ph = PresentationHandler()
    ph.create_presentation(t.topic, ["bart-large-cnn"],
                           {"bart-large-cnn": {}})

    ph.export_presentation()
    #
    # ph.reset()
    # t.topic.title += " p2s"
    # ph.create_presentation(t.topic, ["bart-large-paper-2-slides-summarizer"],
    #                        {"bart-large-paper-2-slides-summarizer": {}})
    # ph.export_presentation()

    # todo: code smells : 1- using strings for encoding, use ENUMs instead.
    # todo: code smells: 2- repeated code, abstract what's repeated
    # todo: code smells: 3- not using built-in functions, ex: list-comprehension
    # todo: code smells: 4- using vague names
    # todo: code smells: 5- using isinstance! causes problems and many if-else
    # todo: code smells: 6- methods with multiple responsibilities!, use <SRP>
    # todo: code smells: 7- adding try-except without handling the exception
    # todo: code smells: 8- don't use built-in errors, use custom error and pass
    #  information to it
    
