class SDes:
    def __init__(self, pbox10, pbox8, ip, epbox, pbox4, chave):
        self.pbox10 = pbox10
        self.pbox8 = pbox8
        self.ip = ip
        self.epbox = epbox
        self.pbox4 = pbox4
        self.chave = chave

    def gerarChaves(self):
        resultadoP10 = self.permutar(self.pbox10, self.chave)
        primeiraParte = self.shift(resultadoP10[:5], 1)
        segundaParte = self.shift(resultadoP10[5:], 1)
        chave1 = self.permutar(self.pbox8, primeiraParte + segundaParte)
        primeiraParte = self.shift(primeiraParte, 2)
        segundaParte = self.shift(segundaParte, 2)
        chave2 = self.permutar(self.pbox8, primeiraParte + segundaParte)
        return (chave1, chave2)

    def cifrar(self, caracter):
        #caracterEmBinario = bin(ord(caracter))[2:].zfill(8)
        caracterEmBinario = '00000011'
        resultadoIP = self.permutar(self.ip, caracterEmBinario)
        segundaParte = resultadoIP[4:]
        resultadoEPBox = self.permutar(self.epbox, segundaParte)
        resultadoXOR = self.xor(resultadoEPBox, '10000001')
        print(resultadoXOR)

    def permutar(self, pbox, bits):
        resultado = list()
        for i in pbox:
            resultado.append(bits[i - 1])
        return resultado
    
    def shift(self, array, quantidade):
        quantidade = quantidade % len(array)
        return array[quantidade:] + array[:quantidade]
        
    def xor(self, bits1, bits2):
        resultado = list()
        for i in range(len(bits1)):
            resultado.append('1') if bits1[i] != bits2[i] else resultado.append('0')
        return resultado