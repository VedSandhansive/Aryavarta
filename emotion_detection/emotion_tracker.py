import time


class EmotionTracker:
    def __init__(self, stable_time=5):
        self.stable_time = stable_time

        self.current_emotion = None
        self.start_time = None

        self.saved = False

    def update(self, emotion):

        now = time.time()

        if emotion != self.current_emotion:
            self.current_emotion = emotion
            self.start_time = now
            self.saved = False
            return False

        if not self.saved and (now - self.start_time) >= self.stable_time:
            self.saved = True
            return True

        return False