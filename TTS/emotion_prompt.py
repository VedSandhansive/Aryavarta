import sys
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from TTS.speaker import speak
from TTS.translator import translate_text


EMOTION_QUESTIONS = {
    "happy": "I see that you are happy. What made you happy today?",

    "sad": "I see that you are feeling sad. Would you like to tell me what happened?",

    "angry": "I sense that you are angry. What is troubling you?",

    "fear": "You seem worried. What are you afraid of?",

    "surprise": "You look surprised. What happened?",

    "neutral": "How are you feeling today?",

    "disgust": "You seem uncomfortable. Would you like to tell me why?"
}


def ask_user_based_on_emotion(language):
    json_paths = [
        PROJECT_ROOT / "emotion.json",
        PROJECT_ROOT / "emotion_state.json",
    ]

    data = None
    for json_path in json_paths:
        if json_path.exists():
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                break
            except Exception as e:
                print(f"[WARN] Failed to read {json_path}: {e}")
                continue

    if data is None:
        print("[ERROR] Emotion file not found.")
        return None

    emotion = data.get("emotion", "neutral").lower()

    question = EMOTION_QUESTIONS.get(
        emotion,
        EMOTION_QUESTIONS["neutral"]
    )

    translated = translate_text(
        question,
        language
    )

    print(f"\nDetected Emotion: {emotion}")
    print(translated)

    try:
        speak(
            translated,
            language
        )
    except Exception as e:
        print(f"[WARN] Speech synthesis failed: {e}")

    return emotion


if __name__ == "__main__":

    language = input("Language : ").lower().strip()

    ask_user_based_on_emotion(language)