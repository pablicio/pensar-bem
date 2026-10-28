from pydantic import BaseModel, field_validator, model_validator


class ProdutoCriar(BaseModel):
    nome: str
    preco: Decimal
    preco_promocional: Decimal | None = None

    @field_validator("nome")
    @classmethod
    def nome_sem_espaco_sobrando(cls, v: str) -> str:
        v = " ".join(v.split())
        if len(v) < 2:
            raise ValueError("nome muito curto")
        return v

    @model_validator(mode="after")
    def promocao_menor_que_preco(self):
        if self.preco_promocional is None:
            return self
        if self.preco_promocional >= self.preco:
            raise ValueError("promoção precisa ser menor que o preço")
        return self
