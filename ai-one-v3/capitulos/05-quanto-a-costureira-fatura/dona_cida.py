import pandas as pd
from sklearn.linear_model import LinearRegression

from visitas import visitas

COLUNAS = ["faturamento_declarado", "idade",
           "tempo_negocio_meses", "emprestimos_anteriores"]

t = visitas()
modelo = LinearRegression().fit(t[COLUNAS],
                                t["faturamento_verificado"])
e = pd.read_csv("dados/brutos/emprestimos.csv")
cida = e[e["cliente_id"] == "C00000"].tail(1)
previsto = modelo.predict(cida[COLUNAS])[0]
for coluna in COLUNAS:
    print(f"{coluna:24} {cida[coluna].iloc[0]:>8}")
print(f"faturamento declarado: R$ "
      f"{cida['faturamento_declarado'].iloc[0]:,.2f}")
print(f"faturamento previsto:  R$ {previsto:,.2f}")
