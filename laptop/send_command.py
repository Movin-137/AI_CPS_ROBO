# laptop/send_commands.py
import socket

def send(cmd, pi_ip="192.168.137.43", port=5051, timeout=5):
    """Send a text command to Raspberry Pi over TCP."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((pi_ip, port))
            sock.sendall(cmd.encode())
            # wait for acknowledgement (optional)
            try:
                reply = sock.recv(1024).decode()
                print(f"[Laptop] Sent command: {cmd} | Reply: {reply}")
            except Exception:
                print(f"[Laptop] Sent command: {cmd} | No reply")
    except Exception as e:
        print(f"[Laptop] Error sending command: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 send_commands.py <command>")
    else:
        send(" ".join(sys.argv[1:]))
