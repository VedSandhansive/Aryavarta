"""
Mode 2
-------
Recites one complete Bhagavad Gita chapter.
"""

import os
import sys

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

    
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


def play_chapter():

    language = input("Enter language: ").lower().strip()

    while True:
        try:
            chapter_number = int(input("Enter chapter number (1-18): "))

            if 1 <= chapter_number <= 18:
                break

            print("Please enter a number between 1 and 18.")

        except ValueError:
            print("Invalid input.")

    chapter = ALL_CHAPTERS[chapter_number - 1]

    chapter_label = translate_text("Chapter", language)
    verse_label = translate_text("Verse", language)
    meaning_label = translate_text("Meaning", language)
    example_label = translate_text("Example", language)

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

        # Sanskrit
        speak(sanskrit, "sanskrit")

        # Meaning
        translated_meaning = translate_text(
            meaning,
            language
        )

        print(f"\n{meaning_label}:")
        print(translated_meaning)

        speak(meaning_label, language)
        speak(translated_meaning, language)

        # Example
        translated_example = translate_text(
            example,
            language
        )

        print(f"\n{example_label}:")
        print(translated_example)

        speak(example_label, language)
        speak(translated_example, language)

    completion = translate_text(
        "Chapter completed.",
        language
    )

    print("\nChapter Completed.")

    speak(completion, language)


if __name__ == "__main__":
    play_chapter()