import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

from polinomios import modelo_polinomial, tres_partes

X_treino, X_valid, y_treino, y_valid = tres_partes()
print(f"treino: {len(X_treino)}   validação: {len(X_valid)}")
print("grau  colunas  erro no treino  erro na validação")
graus, no_treino, na_valid = range(1, 10), [], []
for grau in graus:
    modelo = modelo_polinomial(grau).fit(X_treino, y_treino)
    colunas = len(modelo["prepara"].get_feature_names_out())
    no_treino.append(mean_absolute_error(
        y_treino, modelo.predict(X_treino)))
    na_valid.append(mean_absolute_error(
        y_valid, modelo.predict(X_valid)))
    print(f"{grau:4} {colunas:8} {no_treino[-1]:15,.0f}"
          f" {na_valid[-1]:18,.0f}")

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(graus, no_treino, marker="o", label="treino")
ax.plot(graus, na_valid, marker="o", label="validação")
ax.set_ylim(0, 2000)
ax.set_xlabel("grau dos termos")
ax.set_ylabel("erro absoluto médio (R$)")
ax.set_title("Curva de validação do faturamento")
ax.legend()
fig.tight_layout()
fig.savefig("curva.png", dpi=300)
