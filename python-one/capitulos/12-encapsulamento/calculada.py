class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    @property
    def disponivel(self):
        return self.estoque > 0

    @property
    def valor_em_estoque(self):
        return self.preco * self.estoque
