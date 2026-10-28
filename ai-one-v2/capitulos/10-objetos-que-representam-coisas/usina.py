from dataclasses import dataclass


@dataclass
class Usina:
    nome: str
    potencia_kw: float

    def fator(self, kwh, horas=24):
        return round(kwh / (self.potencia_kw * horas) * 100, 1)


corumba = Usina("Corumbá de Goiás", 2500)
print(corumba)
print(corumba.fator(7772))
