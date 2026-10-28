class ProdutorResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    cidade: str


class ProdutoLer(ProdutoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    criado_em: datetime
    produtor: ProdutorResumo
