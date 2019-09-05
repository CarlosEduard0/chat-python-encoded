from socket import socket, AF_INET, SOCK_STREAM
import threading

def escutarCliente(con):
    while True:
        msg = con.recv(1024)
        if not msg: break
        print(str(msg, 'utf-8'))

def criptografar(msg):
    return msg

tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind(('', 5200))
tcp.listen(1)

print('Servidor iniciado')
print('Aguardando cliente')

conexao, cliente = tcp.accept()
print('Cliente {} conectado'.format(cliente))

threadEscutar = threading.Thread(target = escutarCliente, args = (conexao,))
threadEscutar.start()

mensagem = input()
while True:
    conexao.send(criptografar(mensagem).encode())
    mensagem = input()

threadEscutar.join()
tcp.close()
exit()