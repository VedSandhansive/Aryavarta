"""
Real-Time Face + Gender + Emotion Detection
--------------------------------------------
Combines face_detection.py, gender_detection.py, and emotion_detection.py.

Controls:
    Q → Quit
    S → Save current frame as screenshot
"""

import time
import cv2

from .camera_properties import initialize_camera, resize_display
from .face_detection import detect_faces, draw_box
from .gender_detection import analyze_gender, GENDER_COLORS
from .emotion_detection import load_emotion_model, predict_emotion, EMOTION_COLOR
from .emotion_tracker import EmotionTracker
from .save_emotion import save_emotion

tracker = EmotionTracker(stable_time=3)

# ── Config ────────────────────────────────────────────────────────────
GENDER_ANALYZE_EVERY = 20   # gender (DeepFace) is heavy → throttle hard
EMOTION_ANALYZE_EVERY = 3   # emotion model is light → throttle lightly
FONT = cv2.FONT_HERSHEY_SIMPLEX


def draw_label(frame, text, x, y, color, bg_alpha=0.55):
    (tw, th), baseline = cv2.getTextSize(text, FONT, 0.6, 2)
    pad = 6
    overlay = frame.copy()
    cv2.rectangle(overlay, (x - pad, y - th - pad),
                  (x + tw + pad, y + baseline + pad), color, -1)
    cv2.addWeighted(overlay, bg_alpha, frame, 1 - bg_alpha, 0, frame)
    cv2.putText(frame, text, (x, y), FONT, 0.6, (255, 255, 255), 2, cv2.LINE_AA)


def draw_fps(frame, fps):
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 28), FONT, 0.7,
                (0, 255, 120), 2, cv2.LINE_AA)


def main(auto_exit=True, max_seconds=10):
    cap = initialize_camera()
    load_emotion_model()

    frame_count = 0
    prev_time = time.time()
    start_time = time.time()

    # Stores latest gender/emotion results for each face
    result_cache = []

    # One tracker for each detected face
    trackers = []

    stable_detected = False

    print("[INFO] Press Q to quit | S to save screenshot")

    while True:
        if auto_exit and (time.time() - start_time) >= max_seconds:
            print("[INFO] Auto exit timeout reached.")
            break

        ret, frame = cap.read()

        if not ret:
            print("[WARN] Frame grab failed - retrying...")
            continue

        # Convert YUYV cameras to BGR if needed
        if len(frame.shape) == 3 and frame.shape[2] == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_YUYV)

        frame_count += 1

        faces = detect_faces(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Resize cache and trackers if number of faces changes
        if len(result_cache) != len(faces):
            result_cache = [
                {
                    "gender": ("Unknown", 0.0),
                    "emotion": ("Unknown", 0.0)
                }
                for _ in faces
            ]

            trackers = [
                EmotionTracker(stable_time=5)
                for _ in faces
            ]

        for i, (x, y, w, h) in enumerate(faces):

            face_bgr = frame[y:y+h, x:x+w]
            face_gray = gray[y:y+h, x:x+w]

            if face_bgr.size == 0:
                continue

            # ---------------- Gender Detection ----------------
            if frame_count % GENDER_ANALYZE_EVERY == 0:
                result_cache[i]["gender"] = analyze_gender(face_bgr)

            # ---------------- Emotion Detection ----------------
            if frame_count % EMOTION_ANALYZE_EVERY == 0:
                result_cache[i]["emotion"] = predict_emotion(face_gray)

            gender, gconf = result_cache[i]["gender"]
            emotion, econf = result_cache[i]["emotion"]

            # ---------------- Stable Emotion Check ----------------
            if emotion != "Unknown":
                if trackers[i].update(emotion):
                    print(f"[INFO] Stable emotion detected: {emotion}")

                    save_emotion(
                        emotion=emotion,
                        confidence=econf,
                        gender=gender
                    )
                    stable_detected = True

            # ---------------- Draw Results ----------------
            color = GENDER_COLORS.get(gender, GENDER_COLORS["Unknown"])

            draw_box(frame, x, y, w, h, color=color)

            draw_label(
                frame,
                f"{gender} {gconf:.0f}%",
                x,
                y - 34,
                color
            )

            draw_label(
                frame,
                f"{emotion} {econf:.0f}%",
                x,
                y - 8,
                EMOTION_COLOR
            )

        # ---------------- FPS ----------------
        now = time.time()
        fps = 1.0 / max(now - prev_time, 1e-6)
        prev_time = now

        draw_fps(frame, fps)

        display_frame = resize_display(frame)

        cv2.imshow(
            "Aryavarta Vision | Q=Quit  S=Save",
            display_frame
        )

        if stable_detected and auto_exit:
            print("[INFO] Exiting after stable emotion detected.")
            break

        key = cv2.waitKey(1) & 0xFF
 
        if key == ord("q") or key == ord("Q"):
            break
 
        elif key == ord("s"):
            filename = f"screenshot_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            print(f"[INFO] Saved -> {filename}")

    cap.release()
    cv2.destroyAllWindows()

    print("[INFO] Done.")

if __name__ == "__main__":
    main()
