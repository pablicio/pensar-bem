import numpy as np
from sklearn.linear_model import Lasso

from polinomios import modelo_polinomial, tres_partes

X_treino, X_valid, y_treino, y_valid = tres_partes()
modelo = modelo_polinomial(4)
modelo.set_params(regressao=Lasso(alpha=10, max_iter=50_000))
modelo.fit(X_treino, y_treino)
nomes = modelo["prepara"].get_feature_names_out()
b = modelo["regressao"].coef_
ordem = np.argsort(-np.abs(b))
for i in ordem[:8]:
    nome = nomes[i].split("__")[1]
    print(f"{nome:38} {b[i]:9.1f}")
