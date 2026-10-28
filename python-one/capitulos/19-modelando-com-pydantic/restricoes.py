from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field


class ProdutoCriar(BaseModel):
    nome: Annotated[str, Field(min_length=2, max_length=120)]
    preco: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    estoque: Annotated[int, Field(ge=0)] = 0
