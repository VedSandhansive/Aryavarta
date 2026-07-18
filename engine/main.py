import os
import sys
import json
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from engine.retrieval_engine import run_pipeline
from TTS.verse_speaker import speak_selected_verse


REASON_JSON = os.path.join(BASE_DIR, "STT", "reason.json")


def read_reason():
    """
    Reads the user's problem from STT/reason.json.
    """

    try:
        with open(REASON_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get("reason", "").strip()

    except Exception as e:
        print("[Reason]", e)
        return ""


def handle_request(user_text, emotion="neutral"):
    return run_pipeline(user_text, emotion)


if __name__ == "__main__":

    print("Aryavarta Engine Started...\n")

    while True:

        try:

            # Read the latest reason from STT
            user_text = read_reason()

            if not user_text:
                time.sleep(0.5)
                continue

            print(f"Problem : {user_text}")

            result = handle_request(user_text)

            print(result["response"])

            speak_selected_verse(result)

            # Clear the file after processing
            with open(REASON_JSON, "w", encoding="utf-8") as f:
                json.dump({"reason": ""}, f, indent=4)

            print("\nWaiting for next query...\n")

        except KeyboardInterrupt:
            break

        except Exception as e:
            print(e)
            time.sleep(1)