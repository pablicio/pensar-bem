class UsuarioCriar(BaseModel):
    nome: Annotated[str, Field(min_length=2, max_length=120)]
    email: EmailStr
    senha: Annotated[str, Field(min_length=8, max_length=128)]


class UsuarioLer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    ativo: bool
