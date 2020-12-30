import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 2146        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("connect")
    s.sendall(b'Hello, world')
