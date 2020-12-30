import socket
import struct

# stage 2 clsoe upd and connect tcp


def stage2():
    print("stage2")
    client.close()
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.settimeout(10)
    try:
        clientSocket.connect(('127.0.0.1', 2146))
        print("connected to server")
    except:
        socket.timeout
        print("you just missed it :(")

    Response = clientSocket.recv(1024)
    clientSocket.send(str.encode('Narcomanim!'))
    while True:
        Response = clientSocket.recv(1024)
        print(Response.decode('utf-8'))
        Input = input('')
        clientSocket.send(str.encode(Input))

    clientSocket.close()


# look for server stage 1
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # brodcast
client.bind(("", 13117))
# after 10 sec the window is closed
client.settimeout(10)
print("Client started, listening for offer requests...")


try:
    data, addr = client.recvfrom(1024)  # wait for offer
    message = struct.unpack('Ibh', data)  # unpack offer
    if message[0] == int(0xfeedbeef):          # check cockie
        print("Received offer from ", addr, "attempting to connect... ")
        stage2()
except:
    socket.timeout
    print("you didnt got any offers .. ")
