import RPi.GPIO as GPIO
import time
from raspberry.config import M0_FWD, M0_BWD, M1_FWD, M1_BWD

class MotorController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pins = [M0_FWD, M0_BWD, M1_FWD, M1_BWD]
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def forward(self, dur=0.3):
        GPIO.output(M0_FWD, GPIO.HIGH)
        GPIO.output(M1_FWD, GPIO.HIGH)
        GPIO.output(M0_BWD, GPIO.LOW)
        GPIO.output(M1_BWD, GPIO.LOW)
        time.sleep(dur)
        self.stop()

    def left(self, dur=0.3):
        GPIO.output(M0_BWD, GPIO.HIGH)
        GPIO.output(M1_FWD, GPIO.HIGH)
        time.sleep(dur)
        self.stop()

    def right(self, dur=0.3):
        GPIO.output(M0_FWD, GPIO.HIGH)
        GPIO.output(M1_BWD, GPIO.HIGH)
        time.sleep(dur)
        self.stop()

    def stop(self):
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)

    def cleanup(self):
        self.stop()
        GPIO.cleanup()
