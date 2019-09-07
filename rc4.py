class RC4:
    def __init__(self, chave):
        self.chave = chave
        self.s = [i for i in range(256)]
        self.t = [ord(self.chave[i % len(self.chave)]) for i in range(256)]
        j = 0
        for i in range(256):
            j = (j + self.s[i] + self.t[i]) % 256
            self.s[i], self.s[j] = self.s[j], self.s[i]
    
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
        return chr(ord(caracter) ^ next(self.stream()))
    
    def decifrar(self, caracter):
        return chr(ord(caracter) ^ next(self.stream()))

    def stream(self):
        i = j = 0
        while True:
            i = (i + 1) % 256
            j = (j + self.s[i]) % 256
            self.s[i], self.s[j] = self.s[j], self.s[i]
            t = (self.s[i] + self.s[j]) % 256
            k = self.s[t]
            yield k

    def setChave(self, chave):
        self.__init__(chave)