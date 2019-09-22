import random


class DiffieHellMan:
    def __init__(self, q, a):
        self.q = q
        self.a = a
        self.x = 0
        self.y = 0
        self.k = 0
        self.gerar_chave_privada()
        self.gerar_chave_publica()

    def gerar_chave_privada(self):
        self.x = random.randint(1, self.q - 1)

    def gerar_chave_publica(self):
        self.y = pow(self.a, self.x) % self.q

    def calcular_chave(self, y):
        self.k = pow(y, self.x) % self.q
