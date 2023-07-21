import os.path

import utils as u
from data_preparation_stage import TopicHandler

if __name__ == "__main__":
    t = TopicHandler()
    link = "https://ar.wikipedia.org/wiki/%D8%A7%D9%84%D9%85%D9%84%D8" \
           "%AD%D9%85%D8%A9_%D8%A7%D9%84%D9%83%D8%A8%D8%B1%D9%89"

    t.add_source(link)
