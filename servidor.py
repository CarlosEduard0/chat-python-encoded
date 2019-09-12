from socket import socket, AF_INET, SOCK_STREAM
from SDES import SDes
from rc4 import RC4
import threading

def escutarCliente(con):
    while True:
        msg = con.recv(1024)
        if not msg: break
        msg = algCriptografia.decifrarMensagem(str(msg, 'utf-8'))
        if msg.startswith('chave '):
            trocarChave(msg)
            print('===================================')
            print('=== Chave alterada pelo Cliente ===')
            print('===================================')
        elif msg.startswith('algoritmo '):
            trocarAlgoritmoDeCriptografia(msg)
            print('=======================================')
            print('=== Algoritmo alterado pelo Cliente ===')
            print('=======================================')
        else:
            print('Cliente: {}'.format(msg))

def trocarAlgoritmoDeCriptografia(mensagem):
    global algCriptografia
    algoritmo = mensagem.split(' ')[1]
    chave = mensagem.split(' ')[2]
    if algoritmo == 's-des':
        algCriptografia = SDes(1)
    elif algoritmo == 'rc4':
        algCriptografia = RC4('chave')

def enviarMensagem(mensagem):
    if algCriptografia != None:
        mensagem = algCriptografia.cifrarMensagem(mensagem)
    conexao.send(mensagem.encode())

tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind(('', 5354))
tcp.listen(1)

print('Servidor iniciado')
print('Aguardando cliente')

conexao, cliente = tcp.accept()
print('Cliente {} conectado'.format(cliente))

threadEscutar = threading.Thread(target = escutarCliente, args = (conexao,))
threadEscutar.start()

algCriptografia = SDes(1)

while True:
    mensagem = input()
    enviarMensagem(mensagem)
    if mensagem.startswith('\crypt '):
        trocarAlgoritmoDeCriptografia(mensagem)

threadEscutar.join()
tcp.close()
exit()