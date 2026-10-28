class ProdutorResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    cidade: str


class ProdutoLer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    produtor: ProdutorResumo
