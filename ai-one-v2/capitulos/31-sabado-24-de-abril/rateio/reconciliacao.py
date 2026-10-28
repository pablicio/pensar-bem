"""O que a GED aplicou contra o que devia ter aplicado."""
import pandas as pd

from rateio.calculo import TARIFA
from rateio.geracao import geracao_diaria
from rateio.leitura import BRUTOS, ler_cadastro
from rateio.limpeza import cpf_normalizado

SEDE = "SEDE COOPERSOL CERRADO"


def devido(mes):
    """A geração corrigida e o crédito certo de cada um."""
    geracao = geracao_diaria(mes).groupby("usina")["kwh"]
    geracao = geracao.sum().round(3)
    cad = ler_cadastro()
    ativos = cad[cad["Situação"] == "Ativo"]
    kwh = (ativos["Usina"].map(geracao) * ativos["Cota (%)"]
           / 100).round(2)
    certo = pd.DataFrame({
        "cpf": cpf_normalizado(ativos["CPF"]),
        "nome": ativos["Nome"], "usina": ativos["Usina"],
        "kwh": kwh, "reais": (kwh * TARIFA).round(2)})
    return geracao, certo


def aplicado(mes):
    """O arquivo de compensação da GED: cooperados e sede."""
    arquivo = BRUTOS / f"ged/compensacao/compensacao_{mes}.csv"
    ged = pd.read_csv(arquivo, sep=";", encoding="latin-1",
                      decimal=",", thousands=".",
                      dtype={"CPF": "string"})
    e_sede = ged["Nome"] == SEDE
    cooperados = ged[~e_sede].assign(
        cpf=cpf_normalizado(ged.loc[~e_sede, "CPF"]))
    return cooperados, ged[e_sede].iloc[0]


def reconcilia(mes):
    """O que faltou a cada cooperado, e a linha da sede."""
    geracao, certo = devido(mes)
    cooperados, sede = aplicado(mes)
    lado = certo.merge(cooperados, on="cpf",
                       validate="one_to_one")
    kwh = lado["kwh"] - lado["kWh compensado"]
    return {"lado": lado,
            "faltou": lado["reais"] - lado["Valor (R$)"],
            "faltou_kwh": kwh.sum(),
            "sobra_kwh": geracao.sum() - lado["kwh"].sum(),
            "sede_reais": sede["Valor (R$)"],
            "sede_kwh": sede["kWh compensado"]}
