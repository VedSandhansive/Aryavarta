import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def detect_faces(frame):
    """Detect faces in a BGR frame. Returns list of (x, y, w, h)."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(60, 60)
    )
    return faces


def draw_box(frame, x, y, w, h, color=(0, 255, 0), padding=0):
    """Draw a single bounding box, optionally padded outward."""
    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(frame.shape[1], x + w + padding)
    y2 = min(frame.shape[0], y + h + padding)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    return frame
