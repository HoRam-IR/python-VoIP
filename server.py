import socket
import pyaudio
import threading

HOST = '0.0.0.0'
PORT = 12345

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

clients = set()

def handle_client(client_socket, address):
    print(f"Connection from {address}")

    clients.add(client_socket)

    try:
        while True:
            data = client_socket.recv(CHUNK)
            if not data:
                print(22)
            else:
                for other_socket in clients:
                    if other_socket != client_socket:
                        other_socket.sendall(data)
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        clients.remove(client_socket)
        client_socket.close()
        print(f"Connection with {address} closed")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}")

try:
    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, addr))
        client_handler.start()
except KeyboardInterrupt:
    print("Server shutting down.")
    for socket in clients:
        socket.close()
    server_socket.close()
