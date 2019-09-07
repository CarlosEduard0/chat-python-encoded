import sys
from SDES import SDes
from rc4 import RC4


def menu():
    global modo, nomeArquivoInput, nomeArquivoOutput, algCriptografia
    modo = int(input('Digite o modo de operação\n0 - Cifrar\n1 - Decifrar\n'))
    algoritmo = int(input('Digite o algoritmo que deseja usar\n0 - S-DES\n1 - RC4\n'))
    if algoritmo:
        chave = input('Digite a chave: ')
        algCriptografia = RC4(chave)
    else:
        chave = int(input('Digite um número inteiro para ser a chave: '))
        algCriptografia = SDes(chave)
    if modo:
        nomeArquivoInput = input('Digite o nome  do arquivo criptografado: ')
    else:
        nomeArquivoInput = input('Digite o nome do arquivo em texto claro: ')
    nomeArquivoOutput = input('Digite o nome do arquivo de saída do resultado: ')

modo = 0
nomeArquivoInput = ''
nomeArquivoOutput = ''
algCriptografia = None
menu()

arquivoInput = open(nomeArquivoInput, 'r')
arquivoOutput = open(nomeArquivoOutput, 'w')

while True:
    c = arquivoInput.read(1)
    if not c:
        break;
    if modo:
        arquivoOutput.write(algCriptografia.decifrar(c))
    else:
        arquivoOutput.write(algCriptografia.cifrar(c))

arquivoOutput.close()
arquivoInput.close()
