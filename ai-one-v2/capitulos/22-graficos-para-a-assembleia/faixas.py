import matplotlib.pyplot as plt
import pandas as pd

from rateio.calculo import TARIFA
from rateio.leitura import ler_cadastro

ano = pd.read_csv("dados/processados/geracao_diaria.csv")
fev = ano[ano["data"].str.startswith("2027-02")]
geracao = fev.groupby("usina")["kwh"].sum().round(3)
cad = ler_cadastro()
ativos = cad[cad["Situação"] == "Ativo"]
kwh = ativos["Usina"].map(geracao) * ativos["Cota (%)"] / 100
reais = (kwh.round(2) * TARIFA).round(2)
fig, eixos = plt.subplots(1, 3, figsize=(10, 3))
for ax, faixas in zip(eixos, [10, 40, 200]):
    contagem, _, _ = ax.hist(reais, bins=faixas, color="0.4")
    ax.set_title(f"{faixas} faixas")
    mais_cheia = int(contagem.max())
    print(faixas, "faixas, a mais cheia com", mais_cheia)
fig.savefig("faixas.png", dpi=300, bbox_inches="tight")
