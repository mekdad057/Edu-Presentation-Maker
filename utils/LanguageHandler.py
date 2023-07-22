from langdetect import detect


class LanguageHandler:

    def __init__(self):
        pass

    @staticmethod
    def determine_language(text: str) -> str:
        return detect(text)

    @staticmethod
    def translate(from_lang: str, to_lang: str, text: str) -> str:
        pass
