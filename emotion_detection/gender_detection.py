"""
Gender Detection using OpenCV DNN (Caffe)

Required model files:

models/
├── gender_deploy.prototxt
└── gender_net.caffemodel

Returns:
    ("Male", confidence)
    ("Female", confidence)
"""

import os
from pathlib import Path
import cv2
import numpy as np

# ---------------------------------------------------------------------
# Model Paths (cross-platform compatible)
# ---------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
MODEL_DIR = SCRIPT_DIR / "models"

PROTO_PATH = MODEL_DIR / "gender_deploy.prototxt"
MODEL_PATH = MODEL_DIR / "gender_net.caffemodel"

if not os.path.exists(PROTO_PATH):
    raise FileNotFoundError(
        f"gender_deploy.prototxt not found:\n{PROTO_PATH}"
    )

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"gender_net.caffemodel not found:\n{MODEL_PATH}"
    )

# ---------------------------------------------------------------------
# Load Model Once
# ---------------------------------------------------------------------

print("[INFO] Loading OpenCV Gender Model...")

try:
    gender_net = cv2.dnn.readNetFromCaffe(
        str(PROTO_PATH),
        str(MODEL_PATH)
    )
    print("[INFO] Gender model loaded successfully!")
except Exception as e:
    print(f"[ERROR] Failed to load gender model: {e}")
    raise

# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

GENDER_LABELS = [
    "Male",
    "Female"
]

MODEL_MEAN_VALUES = (
    78.4263377603,
    87.7689143744,
    114.895847746
)

GENDER_COLORS = {
    "Male": (255, 0, 0),       # Blue
    "Female": (255, 0, 255),   # Pink
    "Unknown": (180, 180, 180)
}

# ---------------------------------------------------------------------
# Gender Prediction
# ---------------------------------------------------------------------

def analyze_gender(face_bgr):
    """
    Predict gender from a BGR face image.

    Parameters
    ----------
    face_bgr : numpy.ndarray

    Returns
    -------
    gender : str
    confidence : float
    """

    if face_bgr is None or face_bgr.size == 0:
        return "Unknown", 0.0

    try:
        blob = cv2.dnn.blobFromImage(
            image=face_bgr,
            scalefactor=1.0,
            size=(227, 227),
            mean=MODEL_MEAN_VALUES,
            swapRB=False,
            crop=False
        )

        gender_net.setInput(blob)

        preds = gender_net.forward()

        gender_index = int(np.argmax(preds[0]))

        gender = GENDER_LABELS[gender_index]

        confidence = float(preds[0][gender_index] * 100)

        return gender, confidence

    except Exception as e:
        print(f"[WARN] Gender detection failed: {e}")
        return "Unknown", 0.0