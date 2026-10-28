import matplotlib.pyplot as plt
import pandas as pd

from rateio.calculo import TARIFA
from rateio.geracao import geracao_diaria
from rateio.leitura import ler_cadastro

ano = pd.read_csv("dados/processados/geracao_diaria.csv")
ano["mes"] = ano["data"].str[:7]
mensal = ano.pivot_table(index="mes", columns="usina",
                         values="kwh", aggfunc="sum") / 1000

# 1. a geração de cada mês, empilhada por usina
fig, ax = plt.subplots(figsize=(8, 4))
mensal.plot.bar(stacked=True, ax=ax, width=0.8)
ax.set_xlabel("")
ax.set_ylabel("geração (MWh)")
ax.set_title("Geração mensal, de março/2026 a fevereiro/2027")
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
fig.savefig("mensal.png", dpi=300, bbox_inches="tight")

# 2. março contra março, com dois eixos verticais
marco_2027 = geracao_diaria("2027-03")["kwh"].sum() / 1000
marco = [mensal.loc["2026-03"].sum(), marco_2027]
fig, (esq, dir_) = plt.subplots(1, 2, figsize=(8, 3.5))
for ax, minimo in [(esq, 680), (dir_, 0)]:
    ax.bar(["mar/2026", "mar/2027"], marco, color="0.4")
    ax.set_ylim(minimo, 720)
    ax.set_ylabel("MWh")
    ax.set_title(f"eixo a partir de {minimo}")
fig.savefig("marco.png", dpi=300, bbox_inches="tight")
print(f"março: {marco[0]:.1f} -> {marco[1]:.1f} MWh, "
      f"{marco[1] / marco[0] - 1:+.1%}")

# 3. o crédito de cada cooperado em fevereiro, corrigido
fev = ano[ano["mes"] == "2027-02"]
geracao = fev.groupby("usina")["kwh"].sum().round(3)
cad = ler_cadastro()
ativos = cad[cad["Situação"] == "Ativo"]
kwh = (ativos["Usina"].map(geracao) * ativos["Cota (%)"] / 100)
reais = (kwh.round(2) * TARIFA).round(2)
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.hist(reais, bins=40, color="0.4")
ax.set_xlabel("crédito de fevereiro (R$)")
ax.set_ylabel("cooperados")
fig.savefig("creditos.png", dpi=300, bbox_inches="tight")
print(f"mediana R$ {reais.median():.2f}, "
      f"maior R$ {reais.max():.2f}")
