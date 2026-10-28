import numpy as np
from sklearn.linear_model import Lasso, Ridge
from sklearn.metrics import mean_absolute_error

from polinomios import modelo_polinomial, tres_partes

X_treino, X_valid, y_treino, y_valid = tres_partes()
sem = modelo_polinomial(4).fit(X_treino, y_treino)
erro = mean_absolute_error(y_valid, sem.predict(X_valid))
print(f"sem freio: erro na validação R$ {erro:,.0f}")
print()
print("modelo  alfa  erro na validação  zerados  soma dos |b|")
for nome, classe in [("Ridge", Ridge), ("Lasso", Lasso)]:
    for alfa in [1, 10, 100, 1000]:
        modelo = modelo_polinomial(4)
        modelo.set_params(regressao=classe(alpha=alfa,
                                           max_iter=50_000))
        modelo.fit(X_treino, y_treino)
        b = modelo["regressao"].coef_
        erro = mean_absolute_error(y_valid,
                                   modelo.predict(X_valid))
        zerados = int((np.abs(b) < 1e-8).sum())
        print(f"{nome:6} {alfa:5} {erro:18,.0f} {zerados:8}"
              f" {np.abs(b).sum():13,.0f}")
