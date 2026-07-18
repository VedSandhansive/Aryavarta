import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from data.vedas import rigveda, yajurveda, samaveda, atharvaveda
from TTS.speaker import speak
from TTS.translator import translate_text


VEDAS = {
    1: ("Rigveda", rigveda),
    2: ("Yajurveda", yajurveda),
    3: ("Samaveda", samaveda),
    4: ("Atharvaveda", atharvaveda),
}


def get_collections(module):
    """
    Finds every dictionary in a Veda package that represents
    one Sukta / Adhyaya / Part automatically.
    """

    collections = []

    for name in dir(module):

        if name.startswith("__"):
            continue

        obj = getattr(module, name)

        if isinstance(obj, dict):
            collections.append((name, obj))

    collections.sort(key=lambda x: x[0])

    return collections


def recite_veda():

    language = input("Enter language: ").lower().strip()

    print("""
1. Rigveda
2. Yajurveda
3. Samaveda
4. Atharvaveda
""")

    choice = int(input("Select Veda: "))

    if choice not in VEDAS:
        print("Invalid choice")
        return

    veda_name, module = VEDAS[choice]

    print(f"\nStarting {veda_name}\n")

    speak(veda_name, language)

    collections = get_collections(module)

    for collection_name, hymn in collections:

        print(f"\n{collection_name}")

        speak(
            translate_text(collection_name.replace("_", " "), language),
            language
        )

        for verse_no in sorted(hymn.keys()):

            verse = hymn[verse_no]

            print("\nVerse", verse_no)
            print(verse["sanskrit"])

            speak(
                verse["sanskrit"],
                "sanskrit"
            )

            speak(
                translate_text("Meaning", language),
                language
            )

            speak(
                translate_text(
                    verse["meaning"],
                    language
                ),
                language
            )

            speak(
                translate_text("Example", language),
                language
            )

            speak(
                translate_text(
                    verse["example"],
                    language
                ),
                language
            )

    print("\nCompleted.")


if __name__ == "__main__":
    recite_veda()