class ProdutoLer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    preco: Decimal
