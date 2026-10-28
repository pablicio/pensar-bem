"""Limpeza: unidade, fuso, CPF."""
import pandas as pd


def em_kwh_corumba(df: pd.DataFrame) -> pd.Series:
    """Wh vira kWh, exceto nos dias em que o arquivo já veio em kWh.

    Um inversor de 39 kW gera no máximo ~3,3 kWh em 5 minutos; um dia
    cujo maior valor fica abaixo de 10 só pode estar em kWh."""
    dia = df["inicio"].dt.date
    maximo = df.groupby(dia)["valor"].transform("max")
    return df["valor"].where(maximo < 10, df["valor"] / 1000)


def normaliza_cpf(cpf: pd.Series) -> pd.Series:
    digitos = cpf.astype("string").str.replace(r"\D", "", regex=True)
    return digitos.str.zfill(11)


def cpf_valido(cpf: str) -> bool:
    if len(cpf) != 11 or not cpf.isdigit() or cpf == cpf[0] * 11:
        return False
    d = [int(c) for c in cpf]
    for n in (9, 10):
        soma = sum(v * (n + 1 - i) for i, v in enumerate(d[:n]))
        if soma * 10 % 11 % 10 != d[n]:
            return False
    return True
