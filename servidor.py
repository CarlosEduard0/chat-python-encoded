from socket import socket, AF_INET, SOCK_STREAM
from SDES import SDes
import threading

def escutarCliente(con):
    while True:
        msg = con.recv(1024)
        if not msg: break
        print('Cliente: {}'.format(str(msg, 'utf-8')))
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
    algoritmo = mensagem.split(' ')[1]
    if algoritmo == 's-des':
        algCriptografia = SDes(1)

def trocarChave(mensagem):
    algCriptografia.setChave(int(mensagem.split(' ')[1]))

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
    print('Servidor: {}'.format(algCriptografia.cifrarMensagem(mensagem)))
    conexao.send(algCriptografia.cifrarMensagem(mensagem).encode())
    if mensagem.startswith('chave '):
        trocarChave(mensagem)
    elif mensagem.startswith('algoritmo '):
        trocarAlgoritmoDeCriptografia(mensagem)

threadEscutar.join()
tcp.close()
exit()