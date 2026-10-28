import numpy as np
import pandas as pd

from regioes import divisao
from risco.campeao import COLUNAS_FINAIS, campeao


def por_regiao(valid, nota, fracao=0.60):
    """Aprova a fração de menor risco e mede cada região."""
    v = valid.assign(aprova=nota <= np.quantile(nota, fracao))
    bom = v["alvo"] == 0
    return pd.DataFrame({
        "pedidos": v.groupby("regiao").size(),
        "inadimpl": v.groupby("regiao")["alvo"].mean(),
        "aprova": v.groupby("regiao")["aprova"].mean(),
        "bons recusados": (~v["aprova"])[bom]
        .groupby(v["regiao"]).mean()})


if __name__ == "__main__":
    treino, valid = divisao()
    modelo = campeao()
    modelo.fit(treino[COLUNAS_FINAIS], treino["alvo"])
    nota = modelo.predict_proba(valid[COLUNAS_FINAIS])[:, 1]
    tabela = por_regiao(valid, nota)
    print(tabela.round(3).sort_values("aprova").to_string())
