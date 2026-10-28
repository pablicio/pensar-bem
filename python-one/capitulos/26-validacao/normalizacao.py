from pydantic import field_validator


class ProdutoCriar(BaseModel):
    nome: str
    email_contato: str | None = None

    @field_validator("nome")
    @classmethod
    def limpar_nome(cls, v: str) -> str:
        return " ".join(v.split())

    @field_validator("email_contato")
    @classmethod
    def minusculo(cls, v: str | None) -> str | None:
        return v.strip().lower() if v else None
