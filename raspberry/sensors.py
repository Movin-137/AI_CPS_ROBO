# raspberry/sensors.py
from gpiozero import DistanceSensor

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin, max_distance=2.0):
        # gpiozero uses (echo, trigger)
        self.sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin, max_distance=max_distance)

    def get_distance(self):
        try:
            d_m = self.sensor.distance  # meters or None
            if d_m is None:
                return float('inf')
            return d_m * 100.0
        except Exception:
            return float('inf')

    def close(self):
        try:
            self.sensor.close()
        except Exception:
            pass
