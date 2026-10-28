from sklearn.ensemble import IsolationForest

from recentes import COLUNAS, recentes

r = recentes()
floresta = IsolationForest(n_estimators=500, random_state=0)
floresta.fit(r[COLUNAS])
# score_samples: quanto menor, mais fácil de isolar
r["escore"] = -floresta.score_samples(r[COLUNAS])

curtos = {"valor": "valor", "parcelas": "parc",
          "faturamento_declarado": "faturamento",
          "idade": "idade", "tempo_negocio_meses": "negócio",
          "canal": "canal", "escore": "escore"}
fila = r.sort_values("escore", ascending=False)
print(f"{len(r):,} pedidos; os dez mais estranhos:")
print(fila[list(curtos)].rename(columns=curtos).head(10)
      .round(3).to_string(index=False))
