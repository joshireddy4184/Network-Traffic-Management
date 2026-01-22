import socket
import threading
import time
import random

HOST = '127.0.0.1'
PORT = 5050

send_interval = 0.01  # Normal rate (seconds)
running = True

def listen_server(sock):
    """Listen for server control messages."""
    global send_interval
    while running:
        try:
            message = sock.recv(1024).decode()
            if message == "SLOW_DOWN":
                print("⚠️  Server: Slow down traffic.")
                send_interval = 0.2  # Slow down
            elif message == "RESUME":
                print("✅  Server: Resume normal speed.")
                send_interval = 0.01  # Back to normal
        except:
            break

def start_client(client_id):
    global running
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(f"[CLIENT {client_id}] Connected to server.")

    threading.Thread(target=listen_server, args=(s,), daemon=True).start()

    try:
        while running:
            msg = f"Packet from Client {client_id}"
            s.sendall(msg.encode())
            time.sleep(send_interval + random.uniform(0, 0.01))
    except KeyboardInterrupt:
        running = False
        s.close()
        print(f"[CLIENT {client_id}] Disconnected.")

if __name__ == "__main__":
    client_id = input("Enter client ID: ")
    start_client(client_id)
