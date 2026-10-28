from decimal import Decimal
from typing import Annotated, Literal

from fastapi import Query
from pydantic import BaseModel, Field


class ProdutoFiltro(BaseModel):
    q: str | None = None
    categoria: Categoria | None = None
    preco_min: Annotated[Decimal | None, Field(ge=0)] = None
    preco_max: Annotated[Decimal | None, Field(ge=0)] = None
    apenas_disponiveis: bool = False
    ordenar_por: Literal["nome", "preco", "criado_em"] = "nome"
    ordem: Literal["asc", "desc"] = "asc"
