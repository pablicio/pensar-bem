from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from visitas import NUMEROS, visitas

t = visitas()
X, y = t[NUMEROS], t["faturamento_verificado"]
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.25, random_state=42)
for estrategia in ["mean", "median"]:
    chute = DummyRegressor(strategy=estrategia)
    chute.fit(X_treino, y_treino)
    erro = mean_absolute_error(y_teste, chute.predict(X_teste))
    valor = chute.predict(X_teste[:1])[0]
    print(f"{estrategia:6}  chute R$ {valor:8,.2f}"
          f"  erro no teste R$ {erro:,.2f}")
