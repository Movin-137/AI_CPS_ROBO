import threading
import time
from raspberry.motor_control import MotorController
from raspberry.sensors import UltrasonicSensor
from raspberry.audio_output import speak
from raspberry.config import (
    ULTRA_LEFT_TRIGGER, ULTRA_LEFT_ECHO,
    ULTRA_FRONT_TRIGGER, ULTRA_FRONT_ECHO,
    ULTRA_RIGHT_TRIGGER, ULTRA_RIGHT_ECHO
)

class NavigationController:
    def __init__(self):
        self.motor = MotorController()
        self.left_sensor = UltrasonicSensor(ULTRA_LEFT_TRIGGER, ULTRA_LEFT_ECHO)
        self.front_sensor = UltrasonicSensor(ULTRA_FRONT_TRIGGER, ULTRA_FRONT_ECHO)
        self.right_sensor = UltrasonicSensor(ULTRA_RIGHT_TRIGGER, ULTRA_RIGHT_ECHO)
        self.nav_thread = None
        self.running = False

    def start_nav(self):
        if self.running:
            return
        self.running = True
        self.nav_thread = threading.Thread(target=self._nav_loop)
        self.nav_thread.start()

    def stop_nav(self):
        self.running = False
        speak("Stopping navigation")
        self.motor.stop()

    def _nav_loop(self):
        speak("Starting navigation")
        try:
            while self.running:
                d_left = self.left_sensor.get_distance()
                d_front = self.front_sensor.get_distance()
                d_right = self.right_sensor.get_distance()

                if d_front < 20:
                    speak("Obstacle ahead")
                    if d_left > d_right:
                        self.motor.left(dur=0.5)
                    else:
                        self.motor.right(dur=0.5)
                else:
                    self.motor.forward()
                time.sleep(0.1)
        except Exception as e:
            print("Navigation error:", e)
        finally:
            self.motor.stop()
            self.running = False
