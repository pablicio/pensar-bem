@dataclass
class Produto:
    nome: str
    preco: Decimal
    estoque: int = 0

    def __post_init__(self):
        self.nome = self.nome.strip()
        if not self.nome:
            raise ValueError("nome obrigatório")
        if self.preco <= 0:
            raise ValueError("preço deve ser positivo")
