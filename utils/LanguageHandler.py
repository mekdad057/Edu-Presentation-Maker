from langdetect import detect

class LanguageHandler:

    def __init__(self):
        pass

    def determine_language(self, text: str) -> str:
        return detect(text)

    def translate(self, from_lang: str, to_lang: str, text: str) -> str:
        pass
