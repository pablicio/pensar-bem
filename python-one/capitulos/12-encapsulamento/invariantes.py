class Produto:
    def __init__(self, nome, preco, estoque=0):
        if not nome.strip():
            raise ValueError("nome obrigatório")
        self.nome = nome.strip()
        self._preco = Decimal(preco)
        self._estoque = int(estoque)
        if self._preco <= 0:
            raise ValueError("preço deve ser positivo")
        if self._estoque < 0:
            raise ValueError("estoque não pode ser negativo")

    @property
    def estoque(self):
        return self._estoque

    def repor(self, quantidade):
        if quantidade <= 0:
            raise ValueError("reposição deve ser positiva")
        self._estoque += quantidade

    def vender(self, quantidade):
        if quantidade > self._estoque:
            raise ValueError("estoque insuficiente")
        self._estoque -= quantidade
