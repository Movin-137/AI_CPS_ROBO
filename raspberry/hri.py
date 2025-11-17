# raspberry/hri.py
import socket
from raspberry.config import HRI_SERVER_IP, HRI_PORT

class LLMInteraction:
    def __init__(self):
        self.server_ip = HRI_SERVER_IP
        self.port = HRI_PORT

    def get_response(self, prompt, timeout=10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((self.server_ip, self.port))
                s.sendall(prompt.encode())
                reply = s.recv(8192).decode()
                return reply
        except Exception as e:
            return f"Error contacting HRI server: {e}"
