@dataclass(frozen=True)
class Preco:
    valor: Decimal
    moeda: str = "BRL"
