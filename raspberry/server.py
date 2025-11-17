# raspberry/server.py
import socket
import threading
from raspberry.nav_controller import NavigationController
from raspberry.motor_controller import MotorController
from raspberry.audio_output import speak
from raspberry.config import HOST_IP, COMMAND_PORT
from raspberry.hri import LLMInteraction

nav = NavigationController()
motor = MotorController()
hri_client = LLMInteraction()

def handle_client(conn, addr):
    try:
        data = conn.recv(4096).decode().strip()
        if not data:
            conn.sendall(b"EMPTY")
            return
        print(f"[Server] From {addr}: {data}")
        cmd = data.lower()

        # High-level nav controls
        if cmd in ("start_nav", "navigate"):
            nav.start()
            conn.sendall(b"OK: nav started")
        elif cmd in ("stop_nav", "stop"):
            nav.stop()
            conn.sendall(b"OK: nav stopped")
        elif cmd == "forward":
            motor.forward()
            conn.sendall(b"OK: forward")
        elif cmd in ("back", "backward"):
            motor.backward()
            conn.sendall(b"OK: back")
        elif cmd == "left":
            motor.left_turn()
            conn.sendall(b"OK: left")
        elif cmd == "right":
            motor.right_turn()
            conn.sendall(b"OK: right")
        elif cmd == "hello robot":
            speak("Hello human")
            conn.sendall(b"OK: hello")
        elif cmd.startswith("talk "):
            # Example: "talk how are you?"
            prompt = cmd[len("talk "):].strip()
            reply = hri_client.get_response(prompt)
            # speak reply and also send reply back to caller
            speak(reply)
            conn.sendall(reply.encode())
        else:
            conn.sendall(b"UNKNOWN")
    except Exception as e:
        print("[Server] Error handling client:", e)
    finally:
        try:
            conn.close()
        except Exception:
            pass

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST_IP, COMMAND_PORT))
    s.listen(5)
    print(f"[Server] Listening on {HOST_IP}:{COMMAND_PORT}")
    try:
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("[Server] Shutting down")
    finally:
        s.close()

if __name__ == "__main__":
    start_server()
