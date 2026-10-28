"""Os tipos do rateio."""
from dataclasses import dataclass, field

from rateio.calculo import credito
from rateio.cpf import normaliza_cpf


@dataclass
class Cooperado:
    """Um cooperado: o CPF é a identidade."""
    cpf: str
    nome: str = field(compare=False)
    tipo: str = field(compare=False)
    usina: str = field(compare=False)
    cota_pct: float = field(compare=False)
    situacao: str = field(compare=False, default="Ativo")

    def __post_init__(self):
        self.cpf = normaliza_cpf(self.cpf)
        if not 0 <= self.cota_pct <= 100:
            raise ValueError(f"cota fora de 0 a 100%: "
                             f"{self.cota_pct}")

    def credito(self, geracao):
        return credito(geracao, self.cota_pct)


@dataclass
class Leitura:
    """Uma leitura de 5 minutos de um inversor."""
    usina: str
    inversor: str
    inicio: str
    kwh: float
