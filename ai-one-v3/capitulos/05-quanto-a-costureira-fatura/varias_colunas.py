import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from visitas import visitas

COLUNAS = ["faturamento_declarado", "idade",
           "tempo_negocio_meses", "emprestimos_anteriores"]
t = visitas()
X_treino, X_teste, y_treino, y_teste = train_test_split(
    t[COLUNAS], t["faturamento_verificado"],
    test_size=0.25, random_state=42)

# à mão: uma coluna de uns para o intercepto e lstsq
A = np.column_stack([np.ones(len(X_treino)), X_treino])
coef, *_ = np.linalg.lstsq(A, y_treino, rcond=None)

modelo = LinearRegression().fit(X_treino, y_treino)
sk = np.concatenate([[modelo.intercept_], modelo.coef_])
nomes = ["intercepto"] + COLUNAS
print(pd.DataFrame({"à mão": coef, "scikit-learn": sk},
                   index=nomes).round(3).to_string())

base = DummyRegressor().fit(X_treino, y_treino)
for nome, m in [("chutar a média", base),
                ("regressão", modelo)]:
    erro = mean_absolute_error(y_teste, m.predict(X_teste))
    print(f"{nome:15} erro no teste R$ {erro:8,.2f}")
