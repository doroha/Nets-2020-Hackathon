import struct
import time
from socket import *

Running = False


def client_app():
    global Running
    Running = True

    clientSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)  # udp
    #clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # broadcast
    clientSocket.bind(('', 13117))

    print("Server started,listening on IP address 172.1.0.4")
    # Client receive UDP message (cookie + offer type + TCP PORT)
    data, addr = clientSocket.recvfrom(1024)

    print("server says:")
    print(addr)

    offer = struct.unpack('Ibh', data)
    print(offer)

    # search until you get message with magic cockie
    while offer[0] != 0xFEEDBEEF:
        data, addr = clientSocket.recvfrom(1024)
        offer = struct.unpack('Ibh', data)
        print(offer)

    clientSocket.close()
    address = addr[0]
    print("Received offer from - " + str(address) + " attempting to connect...")

    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        # offer[2] is port number for server tcp
        clientSocket.connect((address, offer[2]))
    except:
        Running = False
        print("you just missed it :(")
        return

    name = "Narckos1\n"
    clientSocket.send(name.encode('ascii'))  # send Team Name

    welcome = clientSocket.recv(1024)  # receive Welcome message:
    print(welcome.decode('ascii'))

    t_end = time.time() + 15
    while time.time() < t_end:
        jibrish = input()
        try:
            clientSocket.send(jibrish.encode('ascii'))
        except:
            continue

    try:
        data = clientSocket.recv(40)  # you typed..
        print(data.decode('ascii'))
    except:
        exit()

    summary = clientSocket.recv(1024) # summary message
    print(summary.decode('ascii'))

    clientSocket.close()
    print("Server disconnected, listening for offer requests. . .\n")
    Running = False


while not Running:
    client_app()
    time.sleep(8)
