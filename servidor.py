from socket import socket, AF_INET, SOCK_STREAM
import threading
from SDES import SDes
from rc4 import RC4
from diffie_hellman import DiffieHellMan


class Servidor:
    def __init__(self, host='127.0.0.1', porta=8080, diffie_hellman=None, algCriptografia=None):
        self.host = host
        self.porta = porta
        self.algCriptografia = algCriptografia
        self.conexao = None
        self.cliente = None
        self.diffie_hellman = diffie_hellman

    def iniciar(self):
        tcp = socket(AF_INET, SOCK_STREAM)
        tcp.bind((self.host, self.porta))
        tcp.listen(1)
        print('Servidor iniciado\nAguardando cliente conectar')
        self.conexao, self.cliente = tcp.accept()
        print('Cliente {} conectado'.format(self.cliente))
        self.trocar_chaves_diffie()
        threading.Thread(target=self.escutar_cliente).start()

    def escutar_cliente(self):
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
        chave_publica = int(str(self.conexao.recv(1024), 'utf-8'))
        self.enviar_mensagem(str(self.diffie_hellman.y))
        self.diffie_hellman.calcular_chave(chave_publica)
        self.enviar_mensagem(str(self.diffie_hellman.k))


servidor = Servidor(porta=5354, diffie_hellman=DiffieHellMan(353, 3))
servidor.iniciar()

while True:
    mensagem = input()
    servidor.enviar_mensagem(mensagem)
    servidor.tratar_mensagem(mensagem)
