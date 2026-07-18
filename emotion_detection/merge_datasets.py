import os
import shutil
from tqdm import tqdm

# ==========================
# CONFIGURATION
# ==========================

DATASET1 = "dataset1"
DATASET2 = "dataset2"

OUTPUT = "merged_dataset"

EMOTIONS = [
    "angry",
    "disgust",
    "fear",
    "happy",
    "neutral",
    "sad",
    "surprise"
]

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)

# ==========================
# CREATE OUTPUT FOLDERS
# ==========================

for split in ["train", "test"]:
    for emotion in EMOTIONS:
        os.makedirs(
            os.path.join(OUTPUT, split, emotion),
            exist_ok=True
        )

# ==========================
# COPY FUNCTION
# ==========================

def copy_split(dataset_path, split):

    print(f"\nProcessing {dataset_path}/{split}")

    for emotion in EMOTIONS:

        src_folder = os.path.join(
            dataset_path,
            split,
            emotion
        )

        if not os.path.exists(src_folder):
            print(f"Missing: {src_folder}")
            continue

        dst_folder = os.path.join(
            OUTPUT,
            split,
            emotion
        )

        files = os.listdir(src_folder)

        image_files = [
            f for f in files
            if f.lower().endswith(IMAGE_EXTENSIONS)
        ]

        for i, file in enumerate(
            tqdm(
                image_files,
                desc=f"{split}/{emotion}"
            )
        ):

            src = os.path.join(
                src_folder,
                file
            )

            # Prevent filename collisions
            new_name = (
                f"{os.path.basename(dataset_path)}"
                f"_{i}_{file}"
            )

            dst = os.path.join(
                dst_folder,
                new_name
            )

            shutil.copy2(src, dst)

# ==========================
# MERGE BOTH DATASETS
# ==========================

for dataset in [DATASET1, DATASET2]:

    copy_split(dataset, "train")
    copy_split(dataset, "test")

print("\nMerge complete!")

# ==========================
# SUMMARY
# ==========================

print("\nDataset Summary:\n")

for split in ["train", "test"]:

    print(f"--- {split.upper()} ---")

    total = 0

    for emotion in EMOTIONS:

        folder = os.path.join(
            OUTPUT,
            split,
            emotion
        )

        count = len(os.listdir(folder))

        total += count

        print(
            f"{emotion:<10} : {count}"
        )

    print(f"TOTAL: {total}\n")