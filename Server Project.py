import socket
import threading
import time
import random
import matplotlib.pyplot as plt

HOST = '127.0.0.1'
PORT = 5050
MAX_CLIENTS = 3
THRESHOLD = 50  # Max allowed packets per second

active_clients = []
packet_counts = []
timestamps = []
lock = threading.Lock()
packet_counter = 0
running = True


def handle_client(conn, addr):
    global packet_counter
    print(f"[NEW CONNECTION] {addr} connected.")
    with lock:
        active_clients.append(addr)

    try:
        while running:
            data = conn.recv(1024)
            if not data:
                break
            packet_counter += 1
    except:
        pass
    finally:
        with lock:
            active_clients.remove(addr)
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")


def monitor_traffic():
    global packet_counter
    start_time = time.time()
    while running:
        time.sleep(1)
        current_rate = packet_counter
        packet_counts.append(current_rate)
        timestamps.append(round(time.time() - start_time, 1))
        print(f"[TRAFFIC] {current_rate} packets/sec")

        # Detect congestion
        if current_rate > THRESHOLD:
            print("⚠️ Congestion detected! Slowing down clients...")
        else:
            print("✅ Normal traffic")

        packet_counter = 0


def start_server():
    global running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CLIENTS)
    print(f"[STARTING] Server running on {HOST}:{PORT}")

    threading.Thread(target=monitor_traffic, daemon=True).start()

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        running = False
        print("\n[STOPPING] Server shutting down...")
        plt.plot(timestamps, packet_counts, marker='o')
        plt.title("Network Traffic Rate")
        plt.xlabel("Time (s)")
        plt.ylabel("Packets/sec")
        plt.show()
        server.close()


if __name__ == "__main__":
    start_server()
