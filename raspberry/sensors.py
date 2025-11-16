import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger = trigger_pin
        self.echo = echo_pin
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trigger, False)

    def get_distance(self):
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)

        t0 = time.time()
        while GPIO.input(self.echo) == 0:
            t0 = time.time()

        t1 = time.time()
        while GPIO.input(self.echo) == 1:
            t1 = time.time()

        elapsed = t1 - t0
        distance = (elapsed * 34300) / 2  # cm
        return distance
