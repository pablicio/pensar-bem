import numpy as np
from sklearn.linear_model import LinearRegression

from visitas import visitas

t = visitas()
x = t["faturamento_declarado"].to_numpy()
y = t["faturamento_verificado"].to_numpy()

# mínimos quadrados à mão, com as fórmulas do volume 1
b = (np.sum((x - x.mean()) * (y - y.mean()))
     / np.sum((x - x.mean()) ** 2))
a = y.mean() - b * x.mean()
print(f"à mão:        {a:8.2f} + {b:.4f} x declarado")

X = t[["faturamento_declarado"]]
modelo = LinearRegression().fit(X, y)
a2, b2 = modelo.intercept_, modelo.coef_[0]
print(f"scikit-learn: {a2:8.2f} + {b2:.4f} x declarado")
