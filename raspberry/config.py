# raspberry/config.py
HOST_IP = "192.168.137.43"   # Pi's IP
COMMAND_PORT = 5051

# Motor GPIO Pins (BCM)
M0_FWD = 17
M0_BWD = 18
M1_FWD = 22
M1_BWD = 27

# Ultrasonic sensor pins (trigger, echo)
ULTRA_LEFT_TRIGGER = 23
ULTRA_LEFT_ECHO = 24
ULTRA_FRONT_TRIGGER = 25
ULTRA_FRONT_ECHO = 8
ULTRA_RIGHT_TRIGGER = 7
ULTRA_RIGHT_ECHO = 1

# HRI server running on laptop
HRI_SERVER_IP = "192.168.137.1"   # <-- set to your LAPTOP IP
HRI_PORT = 6005
