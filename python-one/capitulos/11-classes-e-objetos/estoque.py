class Produto:
    def __init__(self, nome, preco, estoque=0):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def repor(self, quantidade):
        if quantidade <= 0:
            raise ValueError("quantidade deve ser positiva")
        self.estoque += quantidade

    def vender(self, quantidade):
        if quantidade > self.estoque:
            raise ValueError("estoque insuficiente")
        self.estoque -= quantidade
