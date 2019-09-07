import sys
from SDES import SDes


def menu():
    global modo, nomeArquivoInput, nomeArquivoOutput
    modo = int(input('Digite o mode de operação\n0 - Cifrar\n1 - Decifrar\n'))
    if modo:
        nomeArquivoInput = input('Digite o nome  do arquivo criptografado: ')
    else:
        nomeArquivoInput = input('Digite o nome do arquivo em texto claro: ')
    nomeArquivoOutput = input('Digite o nome do arquivo de saída do resultado: ')

modo = 0
nomeArquivoInput = ''
nomeArquivoOutput = ''
menu()

arquivoInput = open(nomeArquivoInput, 'r')
arquivoOutput = open(nomeArquivoOutput, 'w')

s = SDes(4)
while True:
    c = arquivoInput.read(1)
    if not c:
        break;
    if modo:
        arquivoOutput.write(s.decifrar(c))
    else:
        arquivoOutput.write(s.cifrar(c))

arquivoOutput.close()
arquivoInput.close()
