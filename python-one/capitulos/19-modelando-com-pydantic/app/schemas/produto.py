class ProdutoCriar(BaseModel):
    nome: str
    preco: Decimal
    estoque: int = 0


class ProdutoLer(BaseModel):
    id: int
    nome: str
    preco: Decimal
    estoque: int
    criado_em: datetime
