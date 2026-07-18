import cv2

INDEX = 0
WIDTH = 640
HEIGHT = 480
FPS = 30
FOURCC = "YUYV"

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 960

def initialize_camera():
    """
    Initialize camera with Raspberry Pi compatibility.
    Supports both CSI and USB cameras.
    """
    cap = cv2.VideoCapture(INDEX)

    if not cap.isOpened():
        raise Exception("Could not open camera! Check: sudo modprobe bcm2835-v4l2")

    # Resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    # FPS
    cap.set(cv2.CAP_PROP_FPS, FPS)
    # FourCC
    cap.set(
        cv2.CAP_PROP_FOURCC,
        cv2.VideoWriter_fourcc(*FOURCC)
    )
    
    print(f"[INFO] Camera initialized: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    return cap
    
def resize_display(frame):
    """Resize frame for display (lightweight operation)."""
    return cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
