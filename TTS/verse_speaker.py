"""
verse_speaker.py (Part 1)

Loads the correct verse file from data/ according to the JSON returned by
retrieval_engine.py.

Raspberry Pi compatible with pathlib for cross-platform paths.
"""
import sys
from pathlib import Path
import importlib.util
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from TTS.speaker import speak
from TTS.translator import translate_text


# -------------------------------------------------------
# Base Paths (Pathlib - cross-platform)
# -------------------------------------------------------

DATA_DIR = PROJECT_ROOT / "data"
GITA_DIR = DATA_DIR / "gita"
VEDA_DIR = DATA_DIR / "vedas"

LANGUAGE_FILE = PROJECT_ROOT / "STT" / "language.json"


def get_selected_language():
    """
    Reads the currently selected language from language.json
    """

    try:
        with open(LANGUAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get("language", "english").lower()

    except FileNotFoundError:
        print(f"[WARN] Language file not found: {LANGUAGE_FILE}")
        return "english"
    except Exception as e:
        print(f"[WARN] Failed to read language: {e}")
        return "english"


def say(text):
    """
    Translate then speak in user's language.
    """

    language = get_selected_language()

    translated = translate_text(text, language)

    speak(translated, language)
# -------------------------------------------------------
# Dynamic Python Import
# -------------------------------------------------------

def load_python_file(filepath):
    """
    Loads any python file directly with error handling.
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    module_name = filepath.stem

    try:
        spec = importlib.util.spec_from_file_location(
            module_name,
            str(filepath)
        )

        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load module: {filepath}")

        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        return module
        
    except Exception as e:
        print(f"[ERROR] Failed to load {filepath}: {e}")
        raise


# -------------------------------------------------------
# Find Dictionary Automatically
# -------------------------------------------------------

def find_dictionary(module):
    """
    Returns BHAGAVAD_GITA_CH2,
    RIGVEDA_M1_S1,
    ATHARVAVEDA_K1_S2,
    etc.
    """

    for name, value in vars(module).items():

        if (
            name.isupper()
            and isinstance(value, dict)
        ):
            return value

    return None


# =======================================================
# GITA LOADER
# =======================================================

def load_gita_verse(chapter, verse):

    filename = GITA_DIR / f"ch{chapter}.py"

    try:
        module = load_python_file(str(filename))

        verse_dict = find_dictionary(module)

        if verse_dict is None:
            return None

        return verse_dict.get(
            str(verse)
        ) or verse_dict.get(
            verse
        )
    except Exception as e:
        print(f"[ERROR] Failed to load Gita verse {chapter}:{verse}: {e}")
        return None


# =======================================================
# RIGVEDA LOADER
# =======================================================

def load_rigveda_verse(
    mandala,
    sukta,
    verse
):

    filename = VEDA_DIR / "rigveda" / f"mandala{mandala}" / f"sukta{sukta}.py"

    try:
        module = load_python_file(str(filename))

        verse_dict = find_dictionary(module)

        if verse_dict is None:
            return None

        return verse_dict.get(
            str(verse)
        ) or verse_dict.get(
            verse
        )
    except Exception as e:
        print(f"[ERROR] Failed to load Rigveda M{mandala}S{sukta}V{verse}: {e}")
        return None


# =======================================================
# ATHARVAVEDA LOADER
# =======================================================

def load_atharvaveda_verse(
    kanda,
    sukta,
    verse
):

    filename = VEDA_DIR / "atharvaveda" / f"kanda{kanda}" / f"sukta{sukta}.py"

    try:
        module = load_python_file(str(filename))

        verse_dict = find_dictionary(module)

        if verse_dict is None:
            return None

        return verse_dict.get(
            str(verse)
        ) or verse_dict.get(
            verse
        )
    except Exception as e:
        print(f"[ERROR] Failed to load Atharvaveda K{kanda}S{sukta}V{verse}: {e}")
        return None
# =======================================================
# KRISHNA YAJURVEDA LOADER
# Folder:
# data/vedas/yajurveda/krishna/kanda1/prapathaka1.py
# =======================================================

def load_krishna_yajurveda_verse(
    kanda,
    prapathaka,
    verse
):

    filename = VEDA_DIR / "yajurveda" / "krishna" / f"kanda{kanda}" / f"prapathaka{prapathaka}.py"

    try:
        module = load_python_file(str(filename))

        verse_dict = find_dictionary(module)

        if verse_dict is None:
            return None

        return verse_dict.get(
            str(verse)
        ) or verse_dict.get(
            verse
        )
    except Exception as e:
        print(f"[ERROR] Failed to load Krishna Yajurveda K{kanda}P{prapathaka}V{verse}: {e}")
        return None


# =======================================================
# SHUKLA YAJURVEDA LOADER
# Folder:
# data/vedas/yajurveda/shukla/adhyaya12.py
# =======================================================

def load_shukla_yajurveda_verse(
    adhyaya,
    verse
):

    filename = VEDA_DIR / "yajurveda" / "shukla" / f"adhyaya{adhyaya}.py"

    try:
        module = load_python_file(str(filename))

        verse_dict = find_dictionary(module)

        if verse_dict is None:
            return None

        return verse_dict.get(
            str(verse)
        ) or verse_dict.get(
            verse
        )
    except Exception as e:
        print(f"[ERROR] Failed to load Shukla Yajurveda A{adhyaya}V{verse}: {e}")
        return None


# =======================================================
# SAMAVEDA LOADER
#
# Supports:
#
# data/vedas/samaveda/purvarcika/aindra.py
# data/vedas/samaveda/purvarcika/agneya.py
#
# data/vedas/samaveda/uttararcika/....
#
# JSON Example:
#
# {
#     "type":"samaveda",
#     "archika":"Purvarcika Aindra",
#     "verse":15
# }
# =======================================================

def load_samaveda_verse(
    archika,
    verse
):

    parts = archika.lower().split()

    if len(parts) < 2:
        return None

    archika_folder = parts[0]
    file_name = "_".join(parts[1:])

    filename = VEDA_DIR / "samaveda" / archika_folder / f"{file_name}.py"

    try:
        module = load_python_file(str(filename))

        verse_dict = find_dictionary(module)

        if verse_dict is None:
            return None

        return verse_dict.get(
            str(verse)
        ) or verse_dict.get(
            verse
        )
    except Exception as e:
        print(f"[ERROR] Failed to load Samaveda {archika}V{verse}: {e}")
        return None
# =======================================================
# LOAD VERSE FROM RETRIEVAL JSON
# =======================================================

def get_selected_verse(result):
    """
    Reads the JSON produced by retrieval_engine.py and
    returns the complete verse dictionary.

    Returns:
        {
            "sanskrit": "...",
            "meaning": "...",
            "example": "..."
        }
    """

    scripture = result["selected_scripture"]

    # ---------------------------------------------------
    # Bhagavad Gita
    # ---------------------------------------------------

    if scripture == "gita":

        if not result["gita"]:
            return None

        item = result["gita"][0]

        return load_gita_verse(

            item["chapter"],

            item["verse"]

        )

    # ---------------------------------------------------
    # Vedas
    # ---------------------------------------------------

    if scripture == "vedas":

        if not result["vedas"]:
            return None

        item = result["vedas"][0]

        vtype = item["type"]

        # ---------------- Rigveda ----------------

        if vtype == "rigveda":

            return load_rigveda_verse(

                item["mandala"],

                item["sukta"],

                item["verse"]

            )

        # ---------------- Atharvaveda ----------------

        elif vtype == "atharvaveda":

            return load_atharvaveda_verse(

                item["kanda"],

                item["sukta"],

                item["verse"]

            )

        # ---------------- Krishna / Shukla Yajurveda ----------------

        elif vtype == "yajurveda":

            if item["branch"] == "krishna":

                return load_krishna_yajurveda_verse(

                    item["kanda"],

                    item["prapathaka"],

                    item["verse"]

                )

            else:

                return load_shukla_yajurveda_verse(

                    item["adhyaya"],

                    item["verse"]

                )

        # ---------------- Samaveda ----------------

        elif vtype == "samaveda":

            return load_samaveda_verse(

                item["archika"],

                item["verse"]

            )

    return None


# =======================================================
# SPEAKING ORDER
# =======================================================

from threading import Thread

def speak_selected_verse(result):

    verse = get_selected_verse(result)

    if verse is None:
        try:
            speak("I could not find the selected verse.", "english")
        except Exception as e:
            print(f"[ERROR] Failed to speak error message: {e}")
        return

    language = get_selected_language()

    translated_intro = None
    translated_meaning = None
    translated_example = None
    translated_ending = None

    # Worker Functions

    def prepare_intro():
        nonlocal translated_intro
        try:
            translated_intro = translate_text(
                result["intro"] + "\n\n" + result["response"],
                language
            )
        except Exception as e:
            print(f"[WARN] Failed to translate intro: {e}")
            translated_intro = result["intro"]

    def prepare_meaning():
        nonlocal translated_meaning
        try:
            translated_meaning = translate_text(
                verse["meaning"],
                language
            )
        except Exception as e:
            print(f"[WARN] Failed to translate meaning: {e}")
            translated_meaning = verse["meaning"]

    def prepare_example():
        nonlocal translated_example
        try:
            translated_example = translate_text(
                verse["example"],
                language
            )
        except Exception as e:
            print(f"[WARN] Failed to translate example: {e}")
            translated_example = verse["example"]

    def prepare_ending():
        nonlocal translated_ending
        try:
            translated_ending = translate_text(
                "May these teachings bring you peace, strength and wisdom.",
                language
            )
        except Exception as e:
            print(f"[WARN] Failed to translate ending: {e}")
            translated_ending = "May these teachings bring you peace, strength and wisdom."

    # Translate intro first

    prepare_intro()

    try:
        speak(translated_intro, language)
    except Exception as e:
        print(f"[ERROR] Failed to speak intro: {e}")

    # Start background translation

    from threading import Thread
    t1 = Thread(target=prepare_meaning)
    t2 = Thread(target=prepare_example)
    t3 = Thread(target=prepare_ending)

    t1.start()
    t2.start()
    t3.start()

    # Speak Sanskrit

    try:
        speak(verse["sanskrit"], "sanskrit")
    except Exception as e:
        print(f"[ERROR] Failed to speak Sanskrit: {e}")

    # Wait only if still translating

    t1.join()
    t2.join()
    t3.join()

    # Speak translated meaning

    try:
        speak(translated_meaning, language)
    except Exception as e:
        print(f"[ERROR] Failed to speak meaning: {e}")

    # Speak translated example

    try:
        speak(translated_example, language)
    except Exception as e:
        print(f"[ERROR] Failed to speak example: {e}")

    # Ending

    try:
        speak(translated_ending, language)
    except Exception as e:
        print(f"[ERROR] Failed to speak ending: {e}")
# =======================================================
# TEST
# =======================================================

if __name__ == "__main__":

    sample = {
        "selected_scripture": "gita",
        "gita": [
            {
                "chapter": 2,
                "verse": 47
            }
        ],

        "vedas": [],
        "intro": "I understand how difficult this feels.",
        "response": "Bhagavad Gita Chapter 2 Verse 47 may help."

    }
    print(build_speaking_text(sample))