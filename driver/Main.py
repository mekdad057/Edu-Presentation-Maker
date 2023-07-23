import os.path

import utils as u
from data_preparation_stage import TopicHandler
from presentation_genrating_stage import PresentationHandler

if __name__ == "__main__":
    t = TopicHandler("writers")
    link = "https://en.wikipedia.org/wiki/List_of_English_writers"
    # link = "https://en.wikipedia.org/wiki/Fyodor_Dostoevsky"
    # link = "https://ar.wikipedia.org/wiki/%D8%A7%D9%84%D9%85%D9%84%D8%AD%D9" \
    #       "%85%D8%A9_%D8%A7%D9%84%D9%83%D8%A8%D8%B1%D9%89"

    t.add_source(link)
    t.start_preprocessing(["List_of_English_writers.html"]
                          , ["normalizer"
                              , "citations_links_remover"
                              , "non_english_remover"])

    print(t.topic.documents[0].paragraphs[0].processed_data)

    ph = PresentationHandler()

    ph.create_presentation(t.topic, ["Sumy"], 6)
    # print(ph.presentation.all_keypoints[0])
