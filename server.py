import socket
import threading
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5000

clients = []
names = []

log_file = open("chat_log.txt", "a")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file.write(f"[{timestamp}] {message}\n")
    log_file.flush()

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break
            broadcast(msg)
            log(msg.decode())
        except:
            break

    index = clients.index(client)
    name = names[index]
    clients.remove(client)
    names.remove(name)
    client.close()
    broadcast(f"{name} left the chat.".encode())
    log(f"{name} left the chat")

def receive_connections():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server started...")
    log("Server started")

    while True:
        client, address = server.accept()
        client.send("NAME".encode())
        name = client.recv(1024).decode()

        names.append(name)
        clients.append(client)

        print(f"{name} joined")
        broadcast(f"{name} joined the chat.".encode())
        log(f"{name} joined")

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()
