class Produto:
    TAXA_PADRAO = 0.12          # da classe: um só, compartilhado

    def __init__(self, nome, preco):
        self.nome = nome        # da instância: um por objeto
        self.preco = preco

    def preco_final(self):
        return self.preco * (1 + Produto.TAXA_PADRAO)
