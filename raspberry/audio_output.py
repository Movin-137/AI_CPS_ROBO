import subprocess

def speak(text):
    safe_text = text.replace('"', '')
    cmd = f'espeak "{safe_text}" --stdout | aplay -q'
    subprocess.run(cmd, shell=True)
