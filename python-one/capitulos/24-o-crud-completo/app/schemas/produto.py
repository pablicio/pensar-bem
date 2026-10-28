from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class ProdutoCriar(BaseModel):
    nome: Annotated[str, Field(min_length=2, max_length=120)]
    preco: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    estoque: Annotated[int, Field(ge=0)] = 0


class ProdutoLer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    preco: Decimal
    estoque: int
    ativo: bool
    criado_em: datetime
