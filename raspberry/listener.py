import socket
import json
from raspberry.nav_controller import NavigationController
from raspberry.hri import LLMInteraction
from raspberry.audio_output import speak
from raspberry.config import HOST_IP, COMMAND_PORT

def start_listener():
    nav = NavigationController()
    llm = LLMInteraction()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST_IP, COMMAND_PORT))
    sock.listen(1)
    print("[Pi] Listening for laptop commands...")

    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024).decode().strip()
        print(f"[Pi] Command: {data}")

        if data == "navigate":
            nav.start_nav()
        elif data == "stop":
            nav.stop_nav()
        else:
            reply = llm.get_response(data)
            speak(reply)
        conn.close()
