import socket
import struct
import time

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

    pleaseWait = clientSocket.recv(1024)
    print (pleaseWait)
    clientSocket.settimeout(None)
    clientSocket.send(str.encode('Narcomanim!'))
    StartMsg = clientSocket.recv(1024)  #game start
    print(StartMsg)
    EndGameTime=time.time()+10

    

    while time.time()<EndGameTime: 
        Input = input('')
        clientSocket.send(str.encode(Input))
        Response = clientSocket.recv(1024)
        print(Response.decode('utf-8'))

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
        
except:
    socket.timeout
    print("you didnt got any offers .. ")

stage2()
