import os

# ---------------- PATHS ----------------
BASE_DIR = os.getcwd()

DATASET1_PATH = os.path.join(BASE_DIR, "dataset1")
DATASET2_PATH = os.path.join(BASE_DIR, "dataset2")

OUTPUT_PATH = os.path.join(BASE_DIR, "merged_dataset")

TRAIN_PATH = os.path.join(OUTPUT_PATH, "train")
VAL_PATH = os.path.join(OUTPUT_PATH, "val")

# ---------------- CLASSES ----------------
EMOTIONS = [
    "angry",
    "disgust",
    "fear",
    "happy",
    "neutral",
    "sad",
    "surprise"
]

# ---------------- SPLIT ----------------
TRAIN_SPLIT = 0.8