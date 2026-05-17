import asyncio
import edge_tts
import pygame
import time
import uuid
import os
from deep_translator import GoogleTranslator
from data.gita.ch1 import BHAGAVAD_GITA_CH1

# ---------------- COMPLETE LANGUAGE MAP (ONLY GOOGLE TRANSLATE SUPPORTED LANGUAGES) ----------------
# All languages below are VERIFIED from Google Translate's official list
LANG_MAP = {
    # === SOUTH ASIAN LANGUAGES ===
    "hindi": ("hi", "hi-IN-MadhurNeural"),
    "english": ("en", "en-US-AriaNeural"),
    "sanskrit": ("sa", "hi-IN-MadhurNeural"),
    "gujarati": ("gu", "gu-IN-DhwaniNeural"),
    "bengali": ("bn", "bn-IN-TanishaaNeural"),
    "tamil": ("ta", "ta-IN-PallaviNeural"),
    "telugu": ("te", "te-IN-ShrutiNeural"),
    "marathi": ("mr", "mr-IN-AarohiNeural"),
    "kannada": ("kn", "kn-IN-SapnaNeural"),
    "malayalam": ("ml", "ml-IN-SobhanaNeural"),
    "punjabi": ("pa", "pa-IN-OjaasNeural"),
    "urdu": ("ur", "ur-PK-AsadNeural"),
    "odia oriya": ("or", "or-IN-SubasisNeural"),
    "assamese": ("as", "as-IN-PriyomNeural"),
    "sindhi": ("sd", "hi-IN-MadhurNeural"),
    "nepali": ("ne", "ne-NP-HemkalaNeural"),
    "sinhala": ("si", "si-LK-SameeraNeural"),
    "maithili": ("mai", "hi-IN-MadhurNeural"),
    "dogri": ("doi", "hi-IN-MadhurNeural"),
    "kashmiri": ("ks", "hi-IN-MadhurNeural"),
    "konkani": ("gom", "hi-IN-MadhurNeural"),
    "bodo": ("brx", "hi-IN-MadhurNeural"),
    "santhali": ("sat", "hi-IN-MadhurNeural"),
    "bhojpuri": ("bho", "hi-IN-MadhurNeural"),
    "dhivehi": ("dv", "hi-IN-MadhurNeural"),

    # === EAST ASIAN LANGUAGES ===
    "chinese simplified": ("zh-CN", "zh-CN-XiaoxiaoNeural"),
    "chinese traditional": ("zh-TW", "zh-TW-HsiaoChenNeural"),
    "japanese": ("ja", "ja-JP-NanamiNeural"),
    "korean": ("ko", "ko-KR-SunHiNeural"),
    "mongolian": ("mn", "mn-MN-BataaNeural"),
    "tibetan": ("bo", "hi-IN-MadhurNeural"),

    # === SOUTHEAST ASIAN LANGUAGES ===
    "thai": ("th", "th-TH-PremwadeeNeural"),
    "vietnamese": ("vi", "vi-VN-HoaiMyNeural"),
    "indonesian": ("id", "id-ID-GadisNeural"),
    "malay": ("ms", "ms-MY-YasminNeural"),
    "filipino": ("tl", "fil-PH-AngeloNeural"),
    "khmer": ("km", "km-KH-SreymomNeural"),
    "lao": ("lo", "lo-LA-KeomanyNeural"),
    "myanmar burmese": ("my", "my-MM-ThihaNeural"),
    "javanese": ("jw", "jv-ID-SitiNeural"),
    "sundanese": ("su", "su-ID-TutiNeural"),
    "cebuano": ("ceb", "en-US-AriaNeural"),
    "hmong": ("hmn", "en-US-AriaNeural"),

    # === EUROPEAN LANGUAGES ===
    "french": ("fr", "fr-FR-DeniseNeural"),
    "german": ("de", "de-DE-KatjaNeural"),
    "spanish": ("es", "es-ES-ElviraNeural"),
    "italian": ("it", "it-IT-ElsaNeural"),
    "portuguese": ("pt", "pt-BR-FranciscaNeural"),
    "russian": ("ru", "ru-RU-DmitryNeural"),
    "ukrainian": ("uk", "uk-UA-PolinaNeural"),
    "polish": ("pl", "pl-PL-ZofiaNeural"),
    "dutch": ("nl", "nl-NL-ColetteNeural"),
    "greek": ("el", "el-GR-AthinaNeural"),
    "turkish": ("tr", "tr-TR-EmelNeural"),
    "swedish": ("sv", "sv-SE-SofieNeural"),
    "norwegian": ("no", "nb-NO-PernilleNeural"),
    "danish": ("da", "da-DK-ChristelNeural"),
    "finnish": ("fi", "fi-FI-NooraNeural"),
    "czech": ("cs", "cs-CZ-VlastaNeural"),
    "romanian": ("ro", "ro-RO-AlinaNeural"),
    "hungarian": ("hu", "hu-HU-NoemiNeural"),
    "bulgarian": ("bg", "bg-BG-BorislavNeural"),
    "croatian": ("hr", "hr-HR-GabrijelaNeural"),
    "serbian": ("sr", "sr-RS-NicholasNeural"),
    "slovak": ("sk", "sk-SK-ViktoriaNeural"),
    "slovenian": ("sl", "sl-SI-PetraNeural"),
    "estonian": ("et", "et-EE-AnuNeural"),
    "latvian": ("lv", "lv-LV-EveritaNeural"),
    "lithuanian": ("lt", "lt-LT-OnaNeural"),
    "albanian": ("sq", "sq-AL-IlirNeural"),
    "macedonian": ("mk", "mk-MK-MarijaNeural"),
    "icelandic": ("is", "is-IS-GudrunNeural"),
    "irish": ("ga", "ga-IE-OrlaNeural"),
    "welsh": ("cy", "cy-GB-NiaNeural"),
    "belarusian": ("be", "en-US-AriaNeural"),
    "bosnian": ("bs", "hr-HR-GabrijelaNeural"),
    "corsican": ("co", "fr-FR-DeniseNeural"),
    "esperanto": ("eo", "en-US-AriaNeural"),
    "frisian": ("fy", "nl-NL-ColetteNeural"),
    "luxembourgish": ("lb", "de-DE-KatjaNeural"),
    "maltese": ("mt", "en-US-AriaNeural"),
    "scots gaelic": ("gd", "en-US-AriaNeural"),
    "yiddish": ("yi", "en-US-AriaNeural"),

    # === MIDDLE EASTERN LANGUAGES ===
    "arabic": ("ar", "ar-EG-SalmaNeural"),
    "hebrew": ("iw", "he-IL-AvriNeural"),
    "persian": ("fa", "fa-IR-DilaraNeural"),
    "pashto": ("ps", "ps-AF-LatifaNeural"),
    "kurdish kurmanji": ("ku", "hi-IN-MadhurNeural"),
    "kurdish sorani": ("ckb", "hi-IN-MadhurNeural"),
    "azerbaijani": ("az", "az-AZ-BanuNeural"),
    "georgian": ("ka", "ka-GE-EkaNeural"),
    "kazakh": ("kk", "kk-KZ-AigulNeural"),
    "kyrgyz": ("ky", "en-US-AriaNeural"),
    "tajik": ("tg", "en-US-AriaNeural"),
    "turkmen": ("tk", "en-US-AriaNeural"),
    "uyghur": ("ug", "en-US-AriaNeural"),
    "uzbek": ("uz", "uz-UZ-MadinaNeural"),
    "tatar": ("tt", "en-US-AriaNeural"),

    # === AFRICAN LANGUAGES ===
    "swahili": ("sw", "sw-KE-ZuriNeural"),
    "amharic": ("am", "am-ET-MekdesNeural"),
    "hausa": ("ha", "ha-NG-AminaNeural"),
    "yoruba": ("yo", "yo-NG-AbiolaNeural"),
    "igbo": ("ig", "ig-NG-ChinonsoNeural"),
    "somali": ("so", "so-SO-UbaxNeural"),
    "zulu": ("zu", "zu-ZA-ThandoNeural"),
    "afrikaans": ("af", "af-ZA-AdriNeural"),
    "xhosa": ("xh", "xh-ZA-NovelaneNeural"),
    "bambara": ("bm", "en-US-AriaNeural"),
    "chichewa": ("ny", "en-US-AriaNeural"),
    "ewe": ("ee", "en-US-AriaNeural"),
    "kinyarwanda": ("rw", "en-US-AriaNeural"),
    "lingala": ("ln", "en-US-AriaNeural"),
    "luganda": ("lg", "en-US-AriaNeural"),
    "oromo": ("om", "en-US-AriaNeural"),
    "sepedi": ("nso", "en-US-AriaNeural"),
    "sesotho": ("st", "en-US-AriaNeural"),
    "shona": ("sn", "en-US-AriaNeural"),
    "tigrinya": ("ti", "en-US-AriaNeural"),
    "tsonga": ("ts", "en-US-AriaNeural"),
    "twi": ("ak", "en-US-AriaNeural"),

    # === CENTRAL & SOUTH AMERICAN LANGUAGES ===
    "quechua": ("qu", "es-PE-CamilaNeural"),
    "guarani": ("gn", "es-PY-MarioNeural"),
    "aymara": ("ay", "es-BO-MarceloNeural"),
    "haitian creole": ("ht", "en-US-AriaNeural"),

    # === PACIFIC LANGUAGES (In Google Translate list) ===
    "maori": ("mi", "en-US-AriaNeural"),
    "hawaiian": ("haw", "en-US-AriaNeural"),
    "samoan": ("sm", "en-US-AriaNeural"),

    # === OTHER LANGUAGES ===
    "latin": ("la", "en-US-AriaNeural"),
    "malagasy": ("mg", "en-US-AriaNeural"),
    "meiteilon manipuri": ("mni-Mtei", "hi-IN-MadhurNeural"),
    "mizo": ("lus", "hi-IN-MadhurNeural"),
    "krio": ("kri", "en-US-AriaNeural"),
    "ilocano": ("ilo", "en-US-AriaNeural"),
    "armenian": ("hy", "en-US-AriaNeural"),
    "basque": ("eu", "en-US-AriaNeural"),
    "galician": ("gl", "en-US-AriaNeural"),
}

# ---------------- SPEAK FUNCTION ----------------
async def speak(text, voice):
    file = f"audio_{uuid.uuid4().hex}.mp3"

    tts = edge_tts.Communicate(text, voice)
    await tts.save(file)

    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.3)

    pygame.mixer.quit()

    try:
        os.remove(file)
    except:
        pass

# ---------------- VERSE ----------------
verse = BHAGAVAD_GITA_CH1[2]

sanskrit = verse["sanskrit"]
meaning = verse["meaning"]
example = verse["example"]

# ---------------- STEP 1: SANSKRIT ----------------
print("\n🔱 SANSKRIT SHLOKA:\n")
print(sanskrit)
asyncio.run(speak(sanskrit, "hi-IN-MadhurNeural"))

# ---------------- STEP 2: ASK LANGUAGE (PRINT + SPEAK) ----------------
prompt_text = "In which language do you want meaning and example?"

print("\n👉 " + prompt_text)
asyncio.run(speak(prompt_text, "en-US-AriaNeural"))

print(f"\n📋 Available languages: {len(LANG_MAP)} languages")
print("\n".join(sorted(LANG_MAP.keys())))

# ---------------- USER INPUT ----------------
lang = input("\n💬 Type language: ").lower().strip()

if lang not in LANG_MAP:
    fallback_text = f"Language '{lang}' not found. Defaulting to English."
    print(fallback_text)
    asyncio.run(speak(fallback_text, "en-US-AriaNeural"))
    lang = "english"

lang_code, voice = LANG_MAP[lang]

# ---------------- TRANSLATION ----------------
meaning_tr = GoogleTranslator(source="auto", target=lang_code).translate(meaning)
example_tr = GoogleTranslator(source="auto", target=lang_code).translate(example)

final_text = f"""
Meaning:
{meaning_tr}

Example:
{example_tr}
"""

print("\n--- TRANSLATED OUTPUT ---\n")
print(final_text)

# ---------------- SPEAK RESULT ----------------
asyncio.run(speak(final_text, voice))

print(f"\n✅ Done! Recited in {lang}")