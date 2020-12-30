import socket
import time
import struct
from _thread import *


def sendUDP():

    udpServer = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # udp
    udpServer.setsockopt(
        socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # braodcast
    udpServer.settimeout(0.2)

    offerMessage = struct.pack('Ibh', 0xfeedbeef, 0x2, 2146)
    for x in range(10):
        udpServer.sendto(offerMessage, ('<broadcast>', 13117))
        print("offer sent!")
        time.sleep(1)
    print("goodnight udp")
    udpServer.close()


def threaded_client(connection):
    print("client tread start")
    connection.send(str.encode('Welcome to the Server\n'))
    while True:

        data = connection.recv(2048)
        reply = 'Welcome to Keyboard Spamming Battle Royale.\n Group 1:\n== \n Group2:\n== \n Start pressing keys on your keyboard as fast as you can!! ' + \
            data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
        while True:
            data = connection.recv(2048)
            reply = 'Server Says: ' + data.decode('utf-8')
            if not data:
                break
            connection.sendall(str.encode(reply))
        connection.close()

    connection.close()


tcpServer = socket.socket()
tcpServer.settimeout(10)

ServerPort = 2146
ServerIp_Address = "127.0.0.1"
#ServerIp_Address = "172.1.0/24"

ThreadCount = 0

try:
    tcpServer.bind((ServerIp_Address, ServerPort))
    tcpServer.listen(5)
except socket.error as e:
    print(str(e))

print("Server started,listening on IP address: %s" % ServerIp_Address)

start_new_thread(sendUDP, ())


endtime = time.time() + 10
while time.time() < endtime:
    try:
        clientsocket, address = tcpServer.accept()
        tcpServer.settimeout(None)
        print("got another client!")
        print('Connected to ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (clientsocket, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    except:
        socket.timeout
        print("Timeout raised and caught.")

    # add the name to a tean name array(look at reference )
    # create new thread with each client  start_new_thread(todo-playwithclient (clientsocket))
print("bye")
