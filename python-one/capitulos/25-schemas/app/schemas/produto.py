class ProdutoBase(BaseModel):
    nome: Annotated[str, Field(min_length=2, max_length=120)]
    preco: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    estoque: Annotated[int, Field(ge=0)] = 0


class ProdutoCriar(ProdutoBase):
    pass


class ProdutoAtualizar(BaseModel):
    nome: Annotated[str | None, Field(min_length=2)] = None
    preco: Annotated[Decimal | None, Field(gt=0)] = None
    estoque: Annotated[int | None, Field(ge=0)] = None


class ProdutoLer(ProdutoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ativo: bool
    criado_em: datetime
