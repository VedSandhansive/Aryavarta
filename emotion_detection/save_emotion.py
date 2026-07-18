import json
import time

def save_emotion(emotion, confidence, gender):
    data = {
        "emotion": emotion,
        "confidence": round(confidence, 2),
        "gender": gender,
        "timestamp": time.time()
    }

    with open("emotion_state.json", "w") as f:
        json.dump(data, f, indent=4)

    print("[INFO] Emotion saved.")