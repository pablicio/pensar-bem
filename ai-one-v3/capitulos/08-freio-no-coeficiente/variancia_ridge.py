import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

from polinomios import modelo_polinomial, tres_partes

X_treino, X_valid, y_treino, y_valid = tres_partes()
e = pd.read_csv("dados/brutos/emprestimos.csv")
c = pd.read_csv("dados/brutos/clientes.csv")
cida = e[e["cliente_id"] == "C00000"].tail(1).merge(
    c[["cliente_id", "regiao"]], on="cliente_id")
sorteio = np.random.default_rng(2027)
amostras = [sorteio.choice(len(X_treino), size=600,
                           replace=False) for _ in range(5)]
for nome, freio in [("sem freio", None), ("Ridge 100", 100)]:
    previsoes = []
    for linhas in amostras:
        modelo = modelo_polinomial(4)
        if freio:
            modelo.set_params(regressao=Ridge(alpha=freio))
        X, y = X_treino.iloc[linhas], y_treino.iloc[linhas]
        modelo.fit(X, y)
        previsoes.append(modelo.predict(cida)[0])
    texto = "  ".join(f"{p:9,.0f}" for p in previsoes)
    print(f"{nome:9}: {texto}")
