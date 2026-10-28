from decimal import Decimal


class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self._preco = Decimal(preco)

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, valor):
        valor = Decimal(valor)
        if valor <= 0:
            raise ValueError("preço deve ser positivo")
        self._preco = valor
