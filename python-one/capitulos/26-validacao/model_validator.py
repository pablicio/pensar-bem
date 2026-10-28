from pydantic import model_validator


class PeriodoBusca(BaseModel):
    inicio: date
    fim: date

    @model_validator(mode="after")
    def periodo_coerente(self):
        if self.fim < self.inicio:
            raise ValueError("fim não pode ser antes do início")
        if (self.fim - self.inicio).days > 366:
            raise ValueError("período máximo de um ano")
        return self
