import socket
import time
import struct
from _thread import *

def printGroupNames(group1,group2):
    group1names=''
    for team in group1:
        group1names+=team+" "
    group2names=''
    for team in group2:
        group2names+=team+" "
    str=  'Welcome to Keyboard Spamming Battle Royale \n Group 1 =='+group1names+"\n Group 2 =="+group2names
    return str

        


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
    tcpServer.settimeout(None)


def threaded_client(connection):
    
    #wait for game
    print("client tread start")
    connection.send(str.encode('Welcome to the Server please wait until game starts \n'))
    teamName=str(connection.recv(1024))
    print(str(teamName)+" joined")

    if ThreadCount%2==1:
        group1.append(teamName)
    else:
        group2.append(teamName)

    count=0

    while time.time()<gameStartTime:
        time.sleep(gameStartTime-time.time())  #sleep until begin

    print("game starts")
    connection.send(str.encode(printGroupNames(group1,group2)))
    tcpServer.settimeout(None)
    #game

    
    while time.time()<gameStartTime+10: # while game mode
        data = connection.recv(2048)
        count+=len(data.decode('utf-8'))
        reply = 'Server Says: ' + data.decode('utf-8')
        connection.sendall(str.encode(reply))
        
    print("game ends count= "+ str(count))
    connection.close()

def getTCP_Connections():
    try:
        clientsocket, address = tcpServer.accept()
        print("got another client!")
        print('Connected to ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (clientsocket, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    except:
        socket.timeout


startTime=time.time()
gameStartTime=startTime+10

tcpServer = socket.socket()
tcpServer.settimeout(10)

ServerPort = 2146
ServerIp_Address = "127.0.0.1"
#ServerIp_Address = "172.1.0/24"

ThreadCount = 0
group1=[]
group2=[]

try:
    tcpServer.bind((ServerIp_Address, ServerPort))
    tcpServer.listen(5)
except socket.error as e:
    print(str(e))

print("Server started,listening on IP address: %s" % ServerIp_Address)

start_new_thread(sendUDP, ())



while time.time() < gameStartTime:  # getting tcp connetions
    getTCP_Connections()
    tcpServer.settimeout(None)


print("bye")



