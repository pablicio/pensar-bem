from sklearn.metrics import mean_absolute_error

from polinomios import modelo_polinomial, tres_partes

X_treino, X_valid, y_treino, y_valid = tres_partes()
X_300, y_300 = X_treino[:300], y_treino[:300]
print("grau  erro no treino  erro na validação")
for grau in [1, 3, 5, 7, 9]:
    modelo = modelo_polinomial(grau).fit(X_300, y_300)
    treino = mean_absolute_error(y_300, modelo.predict(X_300))
    previsto = modelo.predict(X_valid)
    valid = mean_absolute_error(y_valid, previsto)
    print(f"{grau:4} {treino:15,.0f} {valid:18,.0f}")
