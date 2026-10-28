"""Correções das fontes brutas."""


def cpf_normalizado(serie):
    """Uma coluna de CPF só com os onze dígitos."""
    digitos = serie.str.replace(r"\D", "", regex=True)
    return digitos.str.zfill(11)


def corumba_em_kwh(a):
    """A coluna Energia do fabricante A, sempre em kWh.

    O firmware exporta em Wh; de 9 a 11/2/2027, exportou em kWh
    (foto do visor e e-mail do fabricante em evidencias/).
    Um dia de máximo abaixo de 10 só pode estar em kWh: em Wh,
    o máximo de um dia de geração passa de algumas centenas.
    """
    maximo = a.groupby("Data")["Energia"].transform("max")
    return a["Energia"].where(maximo < 10, a["Energia"] / 1000)
