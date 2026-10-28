from sklearn.ensemble import IsolationForest

from recentes import COLUNAS, recentes

r = recentes()
colunas = COLUNAS + ["mesmo_telefone"]
floresta = IsolationForest(n_estimators=500, random_state=0)
floresta.fit(r[colunas])
r["escore"] = -floresta.score_samples(r[colunas])

fila = r.sort_values("escore", ascending=False).head(20)
curtos = {"data_concessao": "data", "valor": "valor",
          "parcelas": "parc", "agente": "agente",
          "telefone_referencia": "telefone",
          "mesmo_telefone": "mesmo", "escore": "escore"}
fila = fila[list(curtos)].rename(columns=curtos)
fila["data"] = fila["data"].dt.strftime("%d/%m")
print(fila.round(3).to_string(index=False))
