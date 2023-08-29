import logging
from presentation_maker.data_preparation_stage import TopicHandler
from presentation_maker.presentation_genrating_stage import PresentationHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w"
                        , format="%(levelname)s - %(message)s"
                        , encoding="utf-8")

    t = TopicHandler("Dijkstra")  # FOR TESTING CHANGE HERE

    # link = r"https://en.wikipedia.org/wiki/Sorting_algorithm"
    # link = r"https://en.wikipedia.org/wiki/String_theory"
    link = r"https://www.programiz.com/dsa/dijkstra-algorithm"
    # link = r"https://en.wikipedia.org/wiki/Nuclear_fission"
    # link = r"https://en.wikipedia.org/wiki/Algebra"
    t.add_source(link)

    doc_name = t.topic.documents[0].name

    t.start_preprocessing([doc_name]
                          , ["citations_links_remover"
                              , "non_english_math_safe_remover"
                              , "new_lines_remover"])

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
