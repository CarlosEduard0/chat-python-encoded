import sys
from SDES import SDes

nomeArquivoTextoClaro = sys.argv[1]
arquivoTextoClaro = open(nomeArquivoTextoClaro, 'r')

s = SDes()
s.encriptografar()

arquivoTextoClaro.close()