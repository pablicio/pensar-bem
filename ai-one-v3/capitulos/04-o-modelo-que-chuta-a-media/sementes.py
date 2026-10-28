from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from visitas import NUMEROS, visitas

t = visitas()
X, y = t[NUMEROS], t["faturamento_verificado"]
for semente in [1, 2, 3, 4, 5]:
    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, y, test_size=0.25, random_state=semente)
    chute = DummyRegressor().fit(X_treino, y_treino)
    erro = mean_absolute_error(y_teste, chute.predict(X_teste))
    print(f"semente {semente}: erro no teste R$ {erro:,.2f}")
