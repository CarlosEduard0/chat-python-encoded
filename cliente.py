from socket import socket, AF_INET, SOCK_STREAM
import threading
from SDES import SDes
from rc4 import RC4

class Cliente:
    def conectar(self, host, porta, algCriptografia = None):
        self.conexao = socket(AF_INET, SOCK_STREAM)
        self.conexao.connect((host, porta))
        print('Cliente conectado no servidor {} na porta {}'.format(host, porta))
        threading.Thread(target = self.escutarServidor).start()

    def escutarServidor(self):
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

cliente = Cliente()
cliente.conectar('127.0.0.1', 5355)

while True:
    mensagem = input()
    cliente.enviarMensagem(mensagem)