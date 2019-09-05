from socket import socket,AF_INET,SOCK_STREAM
from threading import Thread
import sys

class Send:
    def init(self):
        self.message = ''
        self.connection = None
        
    def put(self, message):
        self.message = message
        if self.connection != None:
            self.connection.send(str.encode(self.message))


def waitForMessage(tcp, send, host, port):
    target = (host, port)
    tcp.connect(target)
    send.connection = tcp
    print ("Connected to ", host, ':', port)
    while True:
        print ("Server:", str(tcp.recv(1024), 'utf-8'))


# __ main __
serverIP = (str(sys.argv[1]))
sysPort = (int(sys.argv[2]))
user = (str(sys.argv[3]))

mySocket = socket(AF_INET, SOCK_STREAM)
send = Send()

# wait for new messages
process = Thread(target=waitForMessage, args=(mySocket, send, serverIP, sysPort))
process.start()

# send messages
while (True):
    message = input()
    send.put(user + ': ' + message)