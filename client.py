import socket
import struct

# look for server stage 1
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", 13117))
print("Client started, listening for offer requests...")


data, addr = client.recvfrom(1024)  # wait for offer
message = struct.unpack('Ibh', data)  # unpack offer
if message[0] == int(0xfeedbeef):          # check cockie
    print("Received offer from ", addr, "attempting to connect... ")
    client.close()
    clientSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('127.0.0.1', 2146))
    print("connect")
    clientSocket.sendall(b'Narcomanim!\n')


