from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Produto:
    nome: str
    preco: Decimal
    estoque: int = 0
