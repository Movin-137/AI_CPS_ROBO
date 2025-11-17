# raspberry/camera_sensor.py
import cv2

class CameraSensor:
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.prev_frame = None

    def get_frame(self):
        if not self.cap or not self.cap.isOpened():
            return None
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None

    def detect_obstacle(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        if self.prev_frame is None:
            self.prev_frame = gray
            return False
        frame_diff = cv2.absdiff(self.prev_frame, gray)
        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
        motion_level = thresh.sum() / 255
        self.prev_frame = gray
        return motion_level > 500

    def release(self):
        try:
            if self.cap:
                self.cap.release()
        except Exception:
            pass
