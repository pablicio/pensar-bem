import numpy as np
import pandas as pd

from regioes import divisao
from risco.campeao import COLUNAS_FINAIS, campeao

treino, valid = divisao()
modelo = campeao().fit(treino[COLUNAS_FINAIS], treino["alvo"])
nota = modelo.predict_proba(valid[COLUNAS_FINAIS])[:, 1]
v = valid.assign(nota=nota)
# os cortes saem de jul–set; a medida, de out–nov
cedo = v[v["data_concessao"] < "2025-10-01"]
tarde = v[v["data_concessao"] >= "2025-10-01"]

corte = np.quantile(cedo["nota"], 0.60)
bons = cedo[cedo["alvo"] == 0]
# em cada região, o corte que recusa 35% dos bons pagadores
cortes = bons.groupby("regiao")["nota"].quantile(0.65)
limite = tarde["regiao"].map(cortes)
regras = {"um corte": tarde["nota"] <= corte,
          "por região": tarde["nota"] <= limite}

linhas = {}
for nome, aprova in regras.items():
    g = tarde.assign(aprova=aprova).groupby("regiao")
    linhas[nome, "aprova"] = g["aprova"].mean()
    linhas[nome, "inad."] = g.apply(
        lambda d: d.loc[d["aprova"], "alvo"].mean())
    total = tarde.loc[aprova, "alvo"].mean()
    print(f"{nome}: aprova {aprova.mean():.1%},"
          f" inadimplência dos aprovados {total:.2%}")
print()
print(pd.DataFrame(linhas).round(3).to_string())
