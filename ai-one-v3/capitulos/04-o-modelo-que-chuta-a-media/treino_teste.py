import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from visitas import NUMEROS, visitas

t = visitas()
X, y = t[NUMEROS], t["faturamento_verificado"]
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.25, random_state=42)
print(f"treino: {len(X_treino):,}   teste: {len(X_teste):,}")

# o baseline: chutar a média do treino para todo mundo
media = y_treino.mean()
erro_treino = np.abs(y_treino - media).mean()
erro_teste = np.abs(y_teste - media).mean()
print(f"média do treino: R$ {media:,.2f}")
print(f"erro chutando a média, treino: R$ {erro_treino:,.2f}")
print(f"erro chutando a média, teste:  R$ {erro_teste:,.2f}")

icaro = HistGradientBoostingRegressor(
    max_iter=500, learning_rate=0.3, max_leaf_nodes=None,
    max_depth=None, min_samples_leaf=1, early_stopping=False,
    random_state=0)
modelos = {"chutar a média": DummyRegressor(),
           "o modelo do Ícaro": icaro}
print()
print("modelo                 erro no treino  erro no teste")
for nome, modelo in modelos.items():
    modelo.fit(X_treino, y_treino)
    no_treino = mean_absolute_error(y_treino,
                                    modelo.predict(X_treino))
    no_teste = mean_absolute_error(y_teste,
                                   modelo.predict(X_teste))
    print(f"{nome:22} {no_treino:14,.2f} {no_teste:14,.2f}")
