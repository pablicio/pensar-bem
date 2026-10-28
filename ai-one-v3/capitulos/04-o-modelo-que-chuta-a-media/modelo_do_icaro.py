from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

from visitas import NUMEROS, visitas

t = visitas()
X, y = t[NUMEROS], t["faturamento_verificado"]
modelo = HistGradientBoostingRegressor(
    max_iter=500, learning_rate=0.3, max_leaf_nodes=None,
    max_depth=None, min_samples_leaf=1, early_stopping=False,
    random_state=0)
modelo.fit(X, y)
erro = mean_absolute_error(y, modelo.predict(X))
print(f"{len(t):,} visitas, erro médio de R$ {erro:,.2f}")
