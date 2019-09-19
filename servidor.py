from socket import socket, AF_INET, SOCK_STREAM
import threading
from SDES import SDes
from rc4 import RC4

class Servidor:
    def __init__(self, host = '127.0.0.1', porta = 8080, algCriptografia = None):
        self.host = host
        self.porta = porta
        self.algCriptografia = algCriptografia
    
    def iniciar(self):
        tcp = socket(AF_INET, SOCK_STREAM)
        tcp.bind((self.host, self.porta))
        tcp.listen(1)
        print('Servidor iniciado\nAguardando cliente conectar')
        self.conexao, self.cliente = tcp.accept()
        print('Cliente {} conectado'.format(self.cliente))
        threading.Thread(target = self.escutarCliente).start()

    def escutarCliente(self):
        while True:
            mensagem = self.conexao.recv(1024)
            if not mensagem: break
            self.tratarMensagem(str(mensagem, 'utf-8'))

    def tratarMensagem(self, mensagem):
        if mensagem.startswith('\\crypt '):
            mensagem = mensagem.split(' ')
            self.trocarAlgoritmo(mensagem[1], mensagem[2])
        else:
            print(mensagem)

    def trocarAlgoritmo(self, algoritmo, chave):
        if algoritmo == 'sdes':
            self.algCriptografia = SDes(chave)
        elif algoritmo == 'rc4':
            self.algCriptografia = RC4(chave)
        else:
            print('Algoritmo inválido')

    def enviarMensagem(self, mensagem):
        self.conexao.send(mensagem.encode())

servidor = Servidor(porta = 5355)
servidor.iniciar()

while True:
    mensagem = input()
    servidor.enviarMensagem(mensagem)
