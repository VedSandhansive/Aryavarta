import os
from engine.config import *

def check_split(path, name):
    print(f"\n Checking {name}")

    for emotion in EMOTIONS:
        folder = os.path.join(path, emotion)

        if not os.path.exists(folder):
            print(f" MISSING: {emotion}")
            continue

        count = len(os.listdir(folder))
        print(f"{emotion}: {count} images")

def main():
    check_split(TRAIN_PATH, "TRAIN SET")
    check_split(VAL_PATH, "VALIDATION SET")

if __name__ == "__main__":
    main()