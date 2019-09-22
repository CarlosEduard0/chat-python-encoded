from socket import socket, AF_INET, SOCK_STREAM
import threading
from SDES import SDes
from rc4 import RC4
from diffie_hellman import DiffieHellMan


class Cliente:
    def __init__(self, diffie_hellman):
        self.diffie_hellman = diffie_hellman
        self.conexao = None
        self.algCriptografia = None

    def conectar(self, host, porta):
        self.conexao = socket(AF_INET, SOCK_STREAM)
        self.conexao.connect((host, porta))
        print('Cliente conectado no servidor {} na porta {}'.format(host, porta))
        self.trocar_chaves_diffie()
        threading.Thread(target=self.escutar_servidor).start()

    def escutar_servidor(self):
        while True:
            msg = self.conexao.recv(1024)
            if not msg:
                break
            msg = self.receber_mensagem(str(msg, 'utf-8'))
            self.tratar_mensagem(msg)
            print(msg)

    def tratar_mensagem(self, msg):
        if msg.startswith('\\crypt '):
            msg = msg.split(' ')
            self.trocar_algoritmo(msg[1], msg[2] if len(msg) > 2 else None)

    def trocar_algoritmo(self, algoritmo, chave):
        if algoritmo == 'sdes':
            self.algCriptografia = SDes(chave)
        elif algoritmo == 'rc4':
            self.algCriptografia = RC4(chave)
        elif algoritmo == 'none':
            self.algCriptografia = None
        else:
            print('Algoritmo inválido')

    def enviar_mensagem(self, msg):
        if self.algCriptografia is not None:
            msg = self.algCriptografia.cifrarMensagem(msg)
        self.conexao.send(msg.encode())

    def receber_mensagem(self, msg):
        if self.algCriptografia is not None:
            msg = self.algCriptografia.decifrarMensagem(msg)
        return msg

    def trocar_chaves_diffie(self):
        self.enviar_mensagem(str(self.diffie_hellman.y))
        chave_publica = int(str(self.conexao.recv(1024), 'utf-8'))
        self.diffie_hellman.calcular_chave(chave_publica)
        chave_recebida = int(str(self.conexao.recv(2014), 'utf-8'))
        if self.diffie_hellman.k == chave_recebida:
            print('Chaves trocadas com sucesso')
        else:
            print('As chaves geradas não são iguais')
            exit(1)


cliente = Cliente(DiffieHellMan(353, 3))
cliente.conectar('127.0.0.1', 5354)

while True:
    mensagem = input()
    cliente.enviar_mensagem(mensagem)
    cliente.tratar_mensagem(mensagem)
