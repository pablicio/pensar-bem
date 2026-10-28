class Produto:
    def __init__(self, nome, preco):
        self.nome = nome          # público
        self._preco = preco       # interno, por convenção
        self._historico = []      # interno
