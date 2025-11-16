import speech_recognition as sr
from send_command import send

WAKE_WORD = "hey robot"  # Customize as needed
PI_IP = "192.168.0.100"  # Replace with your Pi's IP

def listen_for_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("[VoiceControl] Calibrating ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("[VoiceControl] Ready for wake word.")

    while True:
        try:
            with mic as source:
                print("Listening...")
                audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio).lower()
                print(f"[VoiceControl] Heard: {text}")
            except:
                continue

            if WAKE_WORD in text:
                print("[VoiceControl] Wake word detected! Listening for command...")

                with mic as source:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)

                try:
                    command = recognizer.recognize_google(audio).lower()
                    print(f"[VoiceControl] Command: {command}")
                    send(command, pi_ip=PI_IP)
                except:
                    print("[VoiceControl] Didn't catch a command.")
        except KeyboardInterrupt:
            print("\n[VoiceControl] Stopped.")
            break

if __name__ == "__main__":
    listen_for_commands()
