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


tcpServer = socket.socket()

ServerPort = 2146
ServerIp_Address = "127.0.0.1"
#ServerIp_Address = "172.1.0/24"

try:
    tcpServer.bind((ServerIp_Address, ServerPort))
    tcpServer.listen(5)
except socket.error as e:
    print(str(e))

print("Server started,listening on IP address: %s" % ServerIp_Address)

start_new_thread(sendUDP, ())

while True:
    print("in loop")
    # accept connections from outside
    clientsocket, address = tcpServer.accept()
    print("got another client!")
    name = clientsocket.recv(1024)
    print(name)
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    #ct = client_thread(clientsocket)
    # ct.run()
