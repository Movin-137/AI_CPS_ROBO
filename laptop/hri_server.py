# laptop/hri_server.py
import socket
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import threading

HOST = "0.0.0.0"
PORT = 6005
MODEL_NAME = "EleutherAI/gpt-neo-125M"

print("[HRI] Loading model. This may take some time...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
# keep on CPU; if laptop has GPU you can .to("cuda")
print("[HRI] Model loaded.")

def generate_reply(prompt, max_length=100):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=max_length, num_beams=2)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reply

def handle_conn(conn, addr):
    try:
        data = conn.recv(8192).decode()
        if not data:
            return
        print(f"[HRI] Prompt from {addr}: {data[:80]}")
        reply = generate_reply(data)
        conn.sendall(reply.encode())
    except Exception as e:
        print("[HRI] Error:", e)
    finally:
        try:
            conn.close()
        except Exception:
            pass

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"[HRI] Listening on {HOST}:{PORT}")
    try:
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_conn, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("[HRI] Shutting down")
    finally:
        s.close()

if __name__ == "__main__":
    start_server()
