# laptop/voice_control.py
import speech_recognition as sr
from send_commands import send
import socket

# --- CONFIG ---
PI_IP = "192.168.0.100"     # <--- set your Pi IP
PI_PORT = 5051
WAKE_WORD = "hey robot"
# ----------------

recognizer = sr.Recognizer()
mic = sr.Microphone()

def handle_command_text(cmd_text):
    """
    Decide local actions vs send to Pi.
    Special command patterns:
     - talk <prompt>  -> Ask local LLM server (no sending to Pi)
     - navigate / start_nav / stop_nav / forward / back / left / right / hello robot -> sent to Pi
    """
    cmd_text = cmd_text.lower().strip()
    if cmd_text.startswith("talk "):
        # send to local HRI server port (laptop) and print reply locally
        prompt = cmd_text[len("talk "):].strip()
        reply = ask_local_hri(prompt)
        print("[HRI Reply]", reply)
    else:
        # forward to Pi to execute
        send(cmd_text, pi_ip=PI_IP, port=PI_PORT)

def ask_local_hri(prompt, host="127.0.0.1", port=6005, timeout=10):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            s.sendall(prompt.encode())
            reply = s.recv(8192).decode()
            return reply
    except Exception as e:
        return f"HRI error: {e}"

def listen_for_wake_and_commands():
    with mic as source:
        print("[VoiceControl] Calibrating ambient noise (2s)...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("[VoiceControl] Ready. Say the wake word:", WAKE_WORD)

    while True:
        try:
            with mic as source:
                print("[VoiceControl] Listening for wake word...")
                audio = recognizer.listen(source, timeout=None)

            try:
                text = recognizer.recognize_google(audio).lower()
                print("[VoiceControl] Heard:", text)
            except Exception:
                continue

            if WAKE_WORD in text:
                print("[VoiceControl] Wake word detected. Listening for command...")
                with mic as source:
                    try:
                        audio_cmd = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                        cmd_text = recognizer.recognize_google(audio_cmd).lower()
                        print("[VoiceControl] Command:", cmd_text)
                        handle_command_text(cmd_text)
                    except Exception:
                        print("[VoiceControl] Couldn't capture command.")
        except KeyboardInterrupt:
            print("\n[VoiceControl] Stopped by user.")
            break
        except Exception as e:
            print("[VoiceControl] Error:", e)

if __name__ == "__main__":
    listen_for_wake_and_commands()
