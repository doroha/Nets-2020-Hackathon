import struct
import time
import socket
from _thread import *
import threading

#globals
teams = []
group1 = []
group2 = []
score1 = 0
score2 = 0
clients = []
Finished = False
Start = True
t_count = 0



def printGroupNames(group1):
    group1names = ''
    for team in group1:
        group1names += team+" \n "
    return group1names


def sendUDP():

    udpServer = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # udp
    udpServer.setsockopt(
        socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # braodcast
    udpServer.settimeout(0.2)

    offerMessage = struct.pack('Ibh', 0xfeedbeef, 0x2, 2146)
    for x in range(10):
        udpServer.sendto(offerMessage, ('<broadcast>', 13117))
        time.sleep(1)
    udpServer.close()

    while not Finished:  # ?
        time.sleep(1)


def getTCP_Connections():
    global Finished, Start , t_count
    TCP_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    TCP_server.settimeout(1)

    host = ""
    port = 2146
    TCP_server.bind((host, port))  # bind to ip:port and listen
    print("server listening TCP . . .")
    TCP_server.listen(5)  # listen on address

    while not Finished:
        try:
            clientsocket, address = TCP_server.accept()
        except:
            continue
        print('Connected to :', address[0], ':', address[1])
        t_count += 1
        clients.append(clientsocket)
        start_new_thread(play, (clientsocket,))

    print("Game over, sending out offer requests...")
    Start = True
    TCP_server.close()


def play(connection):
    global Finished ,score1 ,score2
    data = connection.recv(1024)  # recive team name
    teamName = data.decode('ascii')
    print("teamName: "+teamName)
    teams.append(teamName)

    if t_count % 2 == 1:
        group1.append(teamName)
        myGroup = 1
    else:
        group2.append(teamName)
        myGroup = 2

   

    Group_1_score = 0
    Group_2_score = 0

    # if len(group1) == 2 and len(group2) == 2:
    msg = "Welcome to Keyboard Spamming Battle Royal!\n " \
        "Group 1: \n" + printGroupNames(group1) +  "Group 2: \n"  + printGroupNames(group2) + "\n" + \
        "Start pressing keys on your keyboard as fast as you can!!"
    connection.send(msg.encode('ascii'))

    time.sleep(1)

    count = 0
    t_end = time.time() + 10
    data = None
    while time.time() < t_end:
        if data:
            print(data.decode('ascii'))
            count += 1  # conut and print clinet keys
        if time.time() < t_end:
            data = connection.recv(1)

    if myGroup == 1:
        score1 += count
    else:
        score2 += count
    

    time.sleep(1)

    if Group_1_score > Group_2_score:
        winner = 'Group_1'
    else:
        winner = 'Group_2'

    msg = "you pressed: " + str(count) + " keys \n"
    connection.send(msg.encode('ascii'))

    msg = "Group 1 pressed in " + str(score1) + " characters. Group 2 pressed in " + str(score2) + " characters. \n " \
        "the winner is : "+winner

    connection.send(msg.encode('ascii'))

    time.sleep(1)
    connection.close()
    Finished = True


while True:
    if Start:
        Start = False
        Finished = False
        score1 = 0
        score2 = 0
        clients=[]
        group1=[]
        group2=[]
        teams=[]

        t1 = threading.Thread(target=sendUDP)
        t2 = threading.Thread(target=getTCP_Connections)

        t1.start()
        t2.start()

        t1.join()
        t2.join()
