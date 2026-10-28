import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from risco.dados import tabela, treino_validacao

FINANCEIRAS = ["valor", "parcelas", "faturamento_declarado",
               "comprometimento", "atrasos_anteriores",
               "idade"]


def primeiro_modelo(treino):
    logistica = LogisticRegression(C=np.inf, tol=1e-10,
                                   max_iter=10_000)
    modelo = make_pipeline(StandardScaler(), logistica)
    return modelo.fit(treino[FINANCEIRAS], treino["alvo"])


if __name__ == "__main__":
    treino, valid = treino_validacao(tabela())
    modelo = primeiro_modelo(treino)
    escala = modelo[0].scale_
    coef = modelo[-1].coef_[0]
    print("coluna                 desvio  razão de chances")
    for nome, s, b in zip(FINANCEIRAS, escala, coef):
        print(f"{nome:21} {s:7.2f} {np.exp(b):17.2f}")
