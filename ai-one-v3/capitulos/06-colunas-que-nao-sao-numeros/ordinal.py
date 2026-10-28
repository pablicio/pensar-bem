from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (OrdinalEncoder,
                                   StandardScaler)

from pipeline_faturamento import CATEGORICAS, NUMERICAS
from visitas import visitas

t = visitas()
X_treino, X_teste, y_treino, y_teste = train_test_split(
    t[NUMERICAS + CATEGORICAS], t["faturamento_verificado"],
    test_size=0.25, random_state=42)
prepara = ColumnTransformer([
    ("numeros", StandardScaler(), NUMERICAS),
    ("categorias", OrdinalEncoder(), CATEGORICAS)])
modelo = Pipeline([("prepara", prepara),
                   ("regressao", LinearRegression())])
modelo.fit(X_treino, y_treino)
erro = mean_absolute_error(y_teste, modelo.predict(X_teste))
print(f"com códigos 1, 2, 3: R$ {erro:,.2f}")
