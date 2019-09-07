from socket import socket,AF_INET,SOCK_STREAM
from threading import Thread
from SDES import SDes
from rc4 import RC4
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
        msg = tcp.recv(1024)
        if not msg: break
        msg = algCriptografia.decifrarMensagem(str(msg, 'utf-8'))
        if msg.startswith('chave '):
            trocarChave(msg)
            print('====================================')
            print('=== Chave alterada pelo Servidor ===')
            print('====================================')
        elif msg.startswith('algoritmo '):
            trocarAlgoritmoDeCriptografia(msg)
            print('========================================')
            print('=== Algoritmo alterado pelo Servidor ===')
            print('========================================')
        else:
            print('Servidor: {}'.format(msg))

def trocarAlgoritmoDeCriptografia(mensagem):
    global algCriptografia
    algoritmo = mensagem.split(' ')[1]
    if algoritmo == 's-des':
        algCriptografia = SDes(1)
    elif algoritmo == 'rc4':
        algCriptografia = RC4('chave')

def trocarChave(mensagem):
    algCriptografia.setChave(mensagem.split(' ')[1])

# __ main __
serverIP = (str(sys.argv[1]))
sysPort = (int(sys.argv[2]))
user = (str(sys.argv[3]))

mySocket = socket(AF_INET, SOCK_STREAM)
send = Send()

# wait for new messages
process = Thread(target=waitForMessage, args=(mySocket, send, serverIP, sysPort))
process.start()

algCriptografia = SDes(1)

# send messages
while (True):
    message = input()
    send.put(algCriptografia.cifrarMensagem(message))
    if message.startswith('chave '):
        trocarChave(message)
    elif message.startswith('algoritmo '):
        trocarAlgoritmoDeCriptografia(message)