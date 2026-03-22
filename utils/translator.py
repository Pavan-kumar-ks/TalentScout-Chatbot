from googletrans import Translator
from functools import lru_cache
import requests
from config import (
    TRANSLATION_GROQ_API_KEY,
    TRANSLATION_MODEL,
    TRANSLATION_TIMEOUT_SECONDS,
)

translator = Translator()

SUPPORTED_LANGUAGES = {
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "portuguese": "pt",
    "russian": "ru",
    "arabic": "ar",
    "chinese": "zh-cn",
    "japanese": "ja",
    "hindi": "hi",
    "en": "en",
    "es": "es",
    "fr": "fr",
    "de": "de",
    "pt": "pt",
    "ru": "ru",
    "ar": "ar",
    "zh-cn": "zh-cn",
    "zh": "zh-cn",
    "ja": "ja",
    "hi": "hi"
}


def normalize_language(language):
    if not language:
        return "en"
    return SUPPORTED_LANGUAGES.get(str(language).strip().lower(), "en")


@lru_cache(maxsize=4096)
def _translate_cached(text, dest_lang="en", src_lang="auto"):
    if src_lang != "auto" and src_lang == dest_lang:
        return text

    if TRANSLATION_GROQ_API_KEY:
        groq_result = _translate_with_groq(text, dest_lang=dest_lang, src_lang=src_lang)
        if groq_result:
            return groq_result

    if src_lang == "auto":
        return translator.translate(text, dest=dest_lang).text
    return translator.translate(text, src=src_lang, dest=dest_lang).text


def _translate_with_groq(text, dest_lang="en", src_lang="auto"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TRANSLATION_GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    source_label = "auto-detected" if src_lang == "auto" else src_lang
    prompt = (
        "Translate the given text accurately. "
        "Preserve meaning, tone, numbers, names, and formatting. "
        "Return only the translated text without explanations.\n\n"
        f"Source language: {source_label}\n"
        f"Target language: {dest_lang}\n"
        f"Text:\n{text}"
    )

    data = {
        "model": TRANSLATION_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=TRANSLATION_TIMEOUT_SECONDS,
        )
        payload = response.json()
        if "choices" in payload and payload["choices"]:
            return payload["choices"][0]["message"]["content"].strip()
    except Exception:
        return None

    return None


def translate_text(text, dest_lang="en", src_lang="auto"):
    if text is None:
        return ""

    text = str(text)
    if not text.strip():
        return text

    dest_lang = normalize_language(dest_lang)
    src_lang = src_lang if src_lang and src_lang != "auto" else "auto"

    try:
        return _translate_cached(text, dest_lang=dest_lang, src_lang=src_lang)
    except Exception:
        return text


def translate_to_english(text, src_lang="auto"):
    return translate_text(text, dest_lang="en", src_lang=src_lang)


def translate_to_language(text, language="en", src_lang="auto"):
    return translate_text(text, dest_lang=language, src_lang=src_lang)


def detect_language(text):
    try:
        return translator.detect(text).lang
    except Exception:
        return "en"