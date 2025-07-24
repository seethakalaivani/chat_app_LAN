# server.py
import socket
import threading

HOST = '127.0.0.1'
PORT = 55558

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = {}

print(f"Server is running on {HOST}:{PORT} and waiting for connections...")

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:  # Avoid sending back to sender
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "/exit":
                leave_msg = f"{usernames[client]} has left the chat."
                print(leave_msg)
                broadcast(leave_msg, client)
                remove_client(client)
                break
            print(message)
            broadcast(message, client)
        except:
            remove_client(client)
            break

def remove_client(client):
    if client in clients:
        clients.remove(client)
        username = usernames.get(client)
        if username:
            print(f"{username} disconnected.")
            del usernames[client]
        client.close()

def accept_connections():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        username = client.recv(1024).decode('utf-8')
        clients.append(client)
        usernames[client] = username

        print(f"Username of the client is {username}")
        welcome = f"{username} has joined the chat!"
        broadcast(welcome, client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.daemon = True
        thread.start()

accept_connections()
