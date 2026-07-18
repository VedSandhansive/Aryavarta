from deep_translator import GoogleTranslator
from .language import LANG_MAP


def translate_text(text, language):
    """
    Translate text into the requested language.

    Returns translated text.
    """

    language = language.lower().strip()

    if language not in LANG_MAP:
        language = "english"

    lang_code, _ = LANG_MAP[language]

    return GoogleTranslator(
        source="auto",
        target=lang_code
    ).translate(text)

