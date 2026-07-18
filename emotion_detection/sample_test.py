import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# -----------------------------
# Emotion Labels
# -----------------------------
emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Neutral",
    "Sad",
    "Surprise"
]

# -----------------------------
# Open File Picker
# -----------------------------
root = tk.Tk()
root.withdraw()

print("Select your .keras model")
model_path = filedialog.askopenfilename(
    title="Select Keras Model",
    filetypes=[("Keras Model", "*.keras")]
)

if model_path == "":
    print("No model selected.")
    exit()

# -----------------------------
# Load Model
# -----------------------------
model = load_model(model_path)
print("✅ Model Loaded Successfully!")

# -----------------------------
# Select Image
# -----------------------------
while True:
    print("Select an image")
    image_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.avif *jfif *.bmp")
        ]
    )

    if image_path == "":
        print("No image selected.")
        exit()

    # -----------------------------
    # Read Image
    # -----------------------------
    img = cv2.imread(image_path)

    if img is None:
        print("Could not read image.")
        exit()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # -----------------------------
    # Load Face Detector
    # -----------------------------
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30,30)
    )

    if len(faces) == 0:
        print("No face detected!")

    # -----------------------------
    # Predict Emotion
    # -----------------------------
    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        face = cv2.resize(face, (48, 48))
        face = face.astype("float32") / 255.0

        face = np.expand_dims(face, axis=-1)
        face = np.expand_dims(face, axis=0)

        prediction = model.predict(face, verbose=0)

        emotion = emotion_labels[np.argmax(prediction)]
        confidence = np.max(prediction) * 100

        print(f"Emotion: {emotion}")
        print(f"Confidence: {confidence:.2f}%")

        cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)

        cv2.putText(
            img,
            f"{emotion} ({confidence:.1f}%)",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

    # -----------------------------
    # Show Result
    # -----------------------------
    plt.figure(figsize=(8,8))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()