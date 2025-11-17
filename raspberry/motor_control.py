# raspberry/motor_controller.py
from gpiozero import Motor
import time
from raspberry.config import M0_FWD, M0_BWD, M1_FWD, M1_BWD

class MotorController:
    def __init__(self):
        self.left = Motor(forward=M0_FWD, backward=M0_BWD)
        self.right = Motor(forward=M1_FWD, backward=M1_BWD)

    def forward(self, dur=None):
        self.left.forward()
        self.right.forward()
        if dur:
            time.sleep(dur)
            self.stop()

    def left_turn(self, dur=None):
        self.left.backward()
        self.right.forward()
        if dur:
            time.sleep(dur)
            self.stop()

    def right_turn(self, dur=None):
        self.left.forward()
        self.right.backward()
        if dur:
            time.sleep(dur)
            self.stop()

    def backward(self, dur=None):
        self.left.backward()
        self.right.backward()
        if dur:
            time.sleep(dur)
            self.stop()

    def stop(self):
        self.left.stop()
        self.right.stop()

    def cleanup(self):
        self.stop()
