import re
import string

from presentation_maker.data_objects import Document
from presentation_maker.data_preparation_stage.text_preprocessing.Processor \
    import Processor


class PunctuationRemover(Processor):
    __arabic_punctuations: str
    __english_punctuations: str
    __punctuations_list: str

    __arabic_diacritics: re.Pattern[str]

    def __init__(self):
        super().__init__()
        self.__arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
        self.__english_punctuations = string.punctuation
        self.__punctuations_list = self.__arabic_punctuations + \
                                   self.__english_punctuations
        self.__arabic_diacritics = re.compile("""
                                 ّ    | # Tashdid
                                 َ    | # Fatha
                                 ً    | # Tanwin Fath
                                 ُ    | # Damma
                                 ٌ    | # Tanwin Damm
                                 ِ    | # Kasra
                                 ٍ    | # Tanwin Kasr
                                 ْ    | # Sukun
                                 ـ    | #tatwel
                             """, re.VERBOSE)

    def process_document(self, doc: Document):
        for i in range(len(doc.paragraphs)):
            self._texts[i] = self.remove_punctuations(self._texts[i])
            doc.paragraphs[i].processed_data = \
                self.remove_diacritics(self._texts[i])

    def remove_diacritics(self, text):
        text = re.sub(self.__arabic_diacritics, '', text)
        return text

    def remove_punctuations(self, text):
        translator = str.maketrans('', '', self.__punctuations_list)
        return text.translate(translator)
