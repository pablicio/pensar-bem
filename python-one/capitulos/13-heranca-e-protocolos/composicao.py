class Produto:
    def __init__(self, nome, preco, selos=None):
        self.nome = nome
        self.preco = preco
        self.selos = selos or []

    def tem(self, selo):
        return selo in self.selos


tomate = Produto("Tomate", 8.90, selos=["organico", "importado"])
