import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import Lasso

from polinomios import modelo_polinomial, tres_partes

X_treino, X_valid, y_treino, y_valid = tres_partes()
A = modelo_polinomial(4)["prepara"].fit_transform(X_treino)
alfas = np.logspace(-1, 3, 30)
caminhos = []
for alfa in alfas:
    lasso = Lasso(alpha=alfa, max_iter=50_000).fit(A, y_treino)
    caminhos.append(lasso.coef_)
caminhos = np.array(caminhos)
vivos = (np.abs(caminhos) > 1e-8).sum(axis=1)
for alfa, n in zip(alfas[::6], vivos[::6]):
    print(f"alfa {alfa:8.2f}: {n:2} colunas com peso")

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(alfas, caminhos, linewidth=0.8)
ax.set_xscale("log")
ax.set_xlabel("alfa (escala logarítmica)")
ax.set_ylabel("coeficiente")
ax.set_title("Os 93 coeficientes, com o freio apertando")
fig.tight_layout()
fig.savefig("caminhos.png", dpi=300)
