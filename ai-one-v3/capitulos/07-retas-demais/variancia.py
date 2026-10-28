import numpy as np
import pandas as pd

from polinomios import modelo_polinomial, tres_partes

X_treino, X_valid, y_treino, y_valid = tres_partes()
e = pd.read_csv("dados/brutos/emprestimos.csv")
c = pd.read_csv("dados/brutos/clientes.csv")
cida = e[e["cliente_id"] == "C00000"].tail(1).merge(
    c[["cliente_id", "regiao"]], on="cliente_id")
sorteio = np.random.default_rng(2027)
for grau in [1, 6]:
    previsoes = []
    for _ in range(5):
        linhas = sorteio.choice(len(X_treino), size=600,
                                replace=False)
        modelo = modelo_polinomial(grau).fit(
            X_treino.iloc[linhas], y_treino.iloc[linhas])
        previsoes.append(modelo.predict(cida)[0])
    texto = "  ".join(f"{p:8,.0f}" for p in previsoes)
    print(f"grau {grau}: {texto}")
