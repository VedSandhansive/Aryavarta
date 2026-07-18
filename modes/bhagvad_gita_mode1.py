"""
Mode 1
-------
Recites the complete Bhagavad Gita chapter by chapter.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---------------- IMPORT GITA ----------------
from data.gita import (
    BHAGAVAD_GITA_CH1,
    BHAGAVAD_GITA_CH2,
    BHAGAVAD_GITA_CH3,
    BHAGAVAD_GITA_CH4,
    BHAGAVAD_GITA_CH5,
    BHAGAVAD_GITA_CH6,
    BHAGAVAD_GITA_CH7,
    BHAGAVAD_GITA_CH8,
    BHAGAVAD_GITA_CH9,
    BHAGAVAD_GITA_CH10,
    BHAGAVAD_GITA_CH11,
    BHAGAVAD_GITA_CH12,
    BHAGAVAD_GITA_CH13,
    BHAGAVAD_GITA_CH14,
    BHAGAVAD_GITA_CH15,
    BHAGAVAD_GITA_CH16,
    BHAGAVAD_GITA_CH17,
    BHAGAVAD_GITA_CH18
)

# ---------------- IMPORT TTS ----------------
from TTS.speaker import speak
from TTS.translator import translate_text

ALL_CHAPTERS = [
    BHAGAVAD_GITA_CH1,
    BHAGAVAD_GITA_CH2,
    BHAGAVAD_GITA_CH3,
    BHAGAVAD_GITA_CH4,
    BHAGAVAD_GITA_CH5,
    BHAGAVAD_GITA_CH6,
    BHAGAVAD_GITA_CH7,
    BHAGAVAD_GITA_CH8,
    BHAGAVAD_GITA_CH9,
    BHAGAVAD_GITA_CH10,
    BHAGAVAD_GITA_CH11,
    BHAGAVAD_GITA_CH12,
    BHAGAVAD_GITA_CH13,
    BHAGAVAD_GITA_CH14,
    BHAGAVAD_GITA_CH15,
    BHAGAVAD_GITA_CH16,
    BHAGAVAD_GITA_CH17,
    BHAGAVAD_GITA_CH18,
]


def play_full_gita():

    language = input("\nEnter language: ").lower().strip()

    print("\nStarting Bhagavad Gita...\n")

    # Translate labels once
    chapter_label = translate_text("Chapter", language)
    verse_label = translate_text("Verse", language)
    meaning_label = translate_text("Meaning", language)
    example_label = translate_text("Example", language)

    for chapter_number, chapter in enumerate(ALL_CHAPTERS, start=1):

        print("\n" + "=" * 60)
        print(f"{chapter_label} {chapter_number}")
        print("=" * 60)

        speak(f"{chapter_label} {chapter_number}", language)

        for verse_number in sorted(chapter.keys()):

            verse = chapter[verse_number]

            sanskrit = verse["sanskrit"]
            meaning = verse["meaning"]
            example = verse["example"]

            print(f"\n{chapter_label} {chapter_number} | {verse_label} {verse_number}")
            print(sanskrit)

            # Speak Sanskrit shloka
            speak(sanskrit, "sanskrit")

            # Translate Meaning
            translated_meaning = translate_text(
                meaning,
                language
            )

            print(f"\n{meaning_label}:")
            print(translated_meaning)

            speak(meaning_label, language)
            speak(translated_meaning, language)

            # Translate Example
            translated_example = translate_text(
                example,
                language
            )

            print(f"\n{example_label}:")
            print(translated_example)

            speak(example_label, language)
            speak(translated_example, language)

    print("\nBhagavad Gita Completed.")

    completion = translate_text(
        "Bhagavad Gita completed.",
        language
    )

    speak(completion, language)


if __name__ == "__main__":
    play_full_gita()