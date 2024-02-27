import socket
import pyaudio

HOST = '127.0.0.1'
PORT = 12345

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

p = pyaudio.PyAudio()

input_stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)

output_stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       output=True,
                       frames_per_buffer=CHUNK)

try:
    while True:
        data = input_stream.read(CHUNK)

        client_socket.sendall(data)

        received_data = client_socket.recv(CHUNK)
        output_stream.write(received_data)
except KeyboardInterrupt:
    print("Client shutting down.")
finally:
    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()
    client_socket.close()
