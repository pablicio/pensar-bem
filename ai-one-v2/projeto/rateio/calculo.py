"""A geração do mês e o rateio pela cota."""
import pandas as pd

from rateio.leitura import (ler_abadiania, ler_cadastro, ler_cocalzinho,
                            ler_corumba)
from rateio.limpeza import em_kwh_corumba, normaliza_cpf

TARIFA = 0.9412


def leituras_do_mes(pasta, mes: str) -> pd.DataFrame:
    a = ler_corumba(pasta, mes)
    a["kwh"] = em_kwh_corumba(a)
    b = ler_cocalzinho(pasta, mes)
    b["kwh"] = b["valor"]
    c = ler_abadiania(pasta, mes)
    c["kwh"] = c["valor"]
    todas = pd.concat([a, b, c], ignore_index=True)
    no_mes = todas["inicio"].dt.strftime("%Y-%m") == mes
    return todas[no_mes]


def geracao(leituras: pd.DataFrame) -> pd.Series:
    positivas = leituras["kwh"].clip(lower=0)
    return positivas.groupby(leituras["usina"]).sum().round(3)


def cooperados_ativos(pasta) -> pd.DataFrame:
    cad = ler_cadastro(pasta)
    cad["cpf"] = normaliza_cpf(cad["CPF"])
    return cad[cad["Situação"] == "Ativo"].copy()


def rateio(pasta, mes: str) -> pd.DataFrame:
    g = geracao(leituras_do_mes(pasta, mes))
    coop = cooperados_ativos(pasta)
    coop["kwh"] = (coop["Usina"].map(g) * coop["Cota (%)"] / 100)
    coop["kwh"] = coop["kwh"].round(2)
    coop["valor"] = (coop["kwh"] * TARIFA).round(2)
    return coop[["cpf", "Nome", "Usina", "Cota (%)", "kwh", "valor"]]
