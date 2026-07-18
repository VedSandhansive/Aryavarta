"""
Emotion detection module (Keras CNN trained on 48x48 grayscale faces).

Your model file was saved in Keras 3's native ".keras" format. Loading
it through `tensorflow.keras` routes to the legacy "tf_keras" shim
(installed because deepface depends on it), and that shim cannot parse
Keras-3-native layer configs (batch_shape, DTypePolicy, etc.) no matter
how many individual fields you patch. The correct fix is to load the
model with the standalone `keras` package (real Keras 3) directly,
bypassing tensorflow.keras entirely.
"""

import os
import cv2
import numpy as np

try:
    import keras  # standalone Keras 3 package, independent of tf_keras
except ImportError as e:
    raise ImportError(
        "The standalone 'keras' package (Keras 3) is required to load this "
        "model correctly. Install it with:\n\n    pip install keras\n"
    ) from e

EMOTION_LABELS = [
    "Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"
]

EMOTION_COLOR = (0, 255, 0)

_model = None


def load_emotion_model(model_filename="models/emotion_classification_model.keras"):
    """Load the trained emotion model once and cache it globally."""
    global _model
    if _model is not None:
        return _model

    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, model_filename)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Emotion model not found at: {model_path}")

    print(f"[INFO] Loading emotion model with Keras {keras.__version__} ...")
    try:
        _model = keras.models.load_model(model_path)
        print("[INFO] Emotion model loaded successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to load emotion model: {e}")
        raise
    return _model


def predict_emotion(face_gray_roi):
    """
    Predict emotion from a grayscale face crop.
    Returns (label, confidence_percent).
    """
    if _model is None:
        raise RuntimeError("Call load_emotion_model() before predict_emotion().")

    face = cv2.resize(face_gray_roi, (48, 48))
    face = face.astype("float32") / 255.0
    face = np.expand_dims(face, axis=-1)  # channel dim
    face = np.expand_dims(face, axis=0)   # batch dim

    prediction = _model.predict(face, verbose=0)
    emotion_index = np.argmax(prediction)
    confidence = float(np.max(prediction) * 100)

    return EMOTION_LABELS[emotion_index], confidence
