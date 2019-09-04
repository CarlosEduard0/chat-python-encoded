import sys
from SDES import SDes

# nomeArquivoTextoClaro = sys.argv[1]
# arquivoTextoClaro = open(nomeArquivoTextoClaro, 'r')

s = SDes(
    [3, 5, 2, 7, 4, 10, 1, 9, 8, 6], # Pbox10
    [6, 3, 7, 4, 8, 5, 10, 9], # Pbox8
    [2, 6, 3, 1, 4, 8, 5, 7], # IP
    [4, 1, 2, 3, 2, 3, 4, 1], # epBox
    [2, 4, 3, 1],
    '1010000010'
)
s.cifrar('a')
# arquivoTextoClaro.close()