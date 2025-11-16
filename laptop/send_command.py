import socket

def send(cmd, pi_ip="192.168.0.100", port=5051):
    """Send a text command to Raspberry Pi over TCP."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((pi_ip, port))
            sock.sendall(cmd.encode())
            print(f"[Laptop] Sent command: {cmd}")
    except Exception as e:
        print(f"[Laptop] Error sending command: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python send_command.py <command>")
    else:
        send(" ".join(sys.argv[1:]))

