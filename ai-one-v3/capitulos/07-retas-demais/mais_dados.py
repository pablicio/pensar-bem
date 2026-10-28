from sklearn.metrics import mean_absolute_error

from polinomios import modelo_polinomial, tres_partes

X_treino, X_valid, y_treino, y_valid = tres_partes()
print("clientes  erro na validação, grau 4")
for n in [300, 600, 900, 1350]:
    modelo = modelo_polinomial(4)
    modelo.fit(X_treino[:n], y_treino[:n])
    previsto = modelo.predict(X_valid)
    erro = mean_absolute_error(y_valid, previsto)
    print(f"{n:8} {erro:26,.0f}")
