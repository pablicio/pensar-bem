class Produto:
    def __init__(self, nome, preco, estoque=0):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def disponivel(self):
        return self.estoque > 0


tomate = Produto("Tomate italiano", 8.90, 120)

print(tomate.nome)
print(tomate.disponivel())
