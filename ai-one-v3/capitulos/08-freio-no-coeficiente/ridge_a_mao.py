import numpy as np
from sklearn.linear_model import Ridge

from polinomios import modelo_polinomial, tres_partes

X_treino, X_valid, y_treino, y_valid = tres_partes()
prepara = modelo_polinomial(4)["prepara"]
A = prepara.fit_transform(X_treino)
y = y_treino.to_numpy()
alfa = 100.0

# à mão: centra as colunas e o alvo, e resolve o sistema
media_A, media_y = A.mean(axis=0), y.mean()
Ac, yc = A - media_A, y - media_y
I = np.eye(A.shape[1])
b = np.linalg.solve(Ac.T @ Ac + alfa * I, Ac.T @ yc)
b0 = media_y - media_A @ b

sk = Ridge(alpha=alfa).fit(A, y)
print(f"{A.shape[1]} colunas, alfa = {alfa:g}")
print(f"intercepto à mão: {b0:10.4f}")
print(f"intercepto sk:    {sk.intercept_:10.4f}")
diferenca = np.abs(b - sk.coef_).max()
print(f"maior diferença nos coeficientes: {diferenca:.1e}")
