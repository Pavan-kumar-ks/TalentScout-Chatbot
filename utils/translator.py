from googletrans import Translator

translator = Translator()


def translate_to_english(text):
    try:
        return translator.translate(text, dest='en').text
    except:
        return text


def detect_language(text):
    try:
        return translator.detect(text).lang
    except:
        return "en"