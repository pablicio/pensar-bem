from sklearn.ensemble import IsolationForest

from recentes import COLUNAS, recentes

r = recentes()
floresta = IsolationForest(n_estimators=500, random_state=0)
floresta.fit(r[COLUNAS])
escore = -floresta.score_samples(r[COLUNAS])
posicao = (-escore).argsort().argsort() + 1
fone = r["telefone_referencia"]
golpe = (fone == "(71) 98877-1203").to_numpy()
print("posições sem o telefone:",
      sorted(posicao[golpe].tolist()))
