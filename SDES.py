class SDes:
    def __init__(self, 
        chave,
        pbox10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6],
        pbox8 = [6, 3, 7, 4, 8, 5, 10, 9],
        ip = [2, 6, 3, 1, 4, 8, 5, 7],
        ip1 = [4, 1, 3, 5, 7, 2, 8, 6], 
        epbox = [4, 1, 2, 3, 2, 3, 4, 1],
        pbox4 = [2, 4, 3, 1],
        s0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]],
        s1 = [[1, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 3], [2, 1, 0, 3]]
    ):
        self.pbox10 = pbox10
        self.pbox8 = pbox8
        self.ip = ip
        self.ip1 = ip1
        self.epbox = epbox
        self.pbox4 = pbox4
        self.chave = chave
        self.s0 = s0
        self.s1 = s1

    def cifrarMensagem(self, mensagem):
        resultado = ''
        for i in mensagem:
            resultado += self.cifrar(i)
        return resultado
    
    def decifrarMensagem(self, mensagem):
        resultado = ''
        for i in mensagem:
            resultado += self.decifrar(i)
        return resultado

    def cifrar(self, caracter):
        caracterEmBinario = bin(ord(caracter))[2:].zfill(8)
        resultadoIP = self.permutar(self.ip, caracterEmBinario)
        resultadoPrimeiraCiclo = self.funcaoFk(self.gerarChaves()[0], resultadoIP[:4], resultadoIP[4:])
        resultadoSegundoCiclo = self.funcaoFk(self.gerarChaves()[1], resultadoPrimeiraCiclo[4:], resultadoPrimeiraCiclo[:4])
        resultadoIP1 = self.permutar(self.ip1, resultadoSegundoCiclo)
        return chr(int(''.join(resultadoIP1), 2))

    def decifrar(self, caracter):
        caracterEmBinario = bin(ord(caracter))[2:].zfill(8)
        resultadoIP = self.permutar(self.ip, caracterEmBinario)
        resultadoPrimeiraCiclo = self.funcaoFk(self.gerarChaves()[1], resultadoIP[:4], resultadoIP[4:])
        resultadoSegundoCiclo = self.funcaoFk(self.gerarChaves()[0], resultadoPrimeiraCiclo[4:], resultadoPrimeiraCiclo[:4])
        resultadoIP1 = self.permutar(self.ip1, resultadoSegundoCiclo)
        return chr(int(''.join(resultadoIP1), 2))

    def gerarChaves(self):
        resultadoP10 = self.permutar(self.pbox10, self.chave)
        primeiraParte = self.shift(resultadoP10[:5], 1)
        segundaParte = self.shift(resultadoP10[5:], 1)
        chave1 = self.permutar(self.pbox8, primeiraParte + segundaParte)
        primeiraParte = self.shift(primeiraParte, 2)
        segundaParte = self.shift(segundaParte, 2)
        chave2 = self.permutar(self.pbox8, primeiraParte + segundaParte)
        return (chave1, chave2)

    def funcaoFk(self, subchave, primeiraParte, segundaParte):
        resultadoEPBox = self.permutar(self.epbox, segundaParte)
        resultadoXOR = self.xor(resultadoEPBox, subchave)
        resultadoS0 = self.executarSbox(resultadoXOR[:4], self.s0)
        resultadoS1 = self.executarSbox(resultadoXOR[4:], self.s1)
        resultadoPBox4 = self.permutar(self.pbox4, resultadoS0 + resultadoS1)
        final = self.xor(resultadoPBox4, primeiraParte)
        return final + segundaParte

    def executarSbox(self, bits, sbox):
        linha = int(bits[0] + bits[3], 2)
        coluna = int(bits[1] + bits[2], 2)
        resultado = sbox[linha][coluna]
        return bin(resultado)[2:].zfill(2)

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
