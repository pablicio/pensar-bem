class ProdutoLer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    criado_em: datetime = Field(alias="createdAt")
