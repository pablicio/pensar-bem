import pandas as pd

from rateio.calculo import TARIFA
from rateio.leitura import ler_cadastro

ano = pd.read_csv("dados/processados/geracao_diaria.csv")
fev = ano[ano["data"].str.startswith("2027-02")]
geracao = fev.groupby("usina")["kwh"].sum().round(3)

cad = ler_cadastro()
ativos = cad[cad["Situação"] == "Ativo"]
kwh = (ativos["Usina"].map(geracao) * ativos["Cota (%)"] / 100)
rateio = ativos.assign(valor=(kwh.round(2) * TARIFA).round(2))
tabela = rateio.pivot_table(index="Tipo", values="valor",
                            aggfunc=["count", "sum"],
                            margins=True, margins_name="total")
print(tabela.round(2))
print(f"soma dos créditos: R$ {rateio['valor'].sum():,.2f}")
