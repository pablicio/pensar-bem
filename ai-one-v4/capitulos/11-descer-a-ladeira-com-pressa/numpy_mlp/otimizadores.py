"""Como dar o passo, depois de saber a direção."""


class SGD:
    """Cada parâmetro anda contra o seu gradiente."""

    def __init__(self, rede, taxa):
        self.rede, self.taxa = rede, taxa

    def passo(self):
        for camada, valor, nome in self.rede.parametros():
            valor -= self.taxa * getattr(camada, nome)
