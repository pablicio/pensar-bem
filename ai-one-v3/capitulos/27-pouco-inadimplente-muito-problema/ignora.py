from sklearn.metrics import accuracy_score, recall_score

from precoce import divisao
from risco.modelos import COLUNAS, logistica

treino, valid = divisao()
print(f"precoce no treino: {treino['precoce'].mean():.1%}"
      f" ({treino['precoce'].sum()} de {len(treino):,})")
modelo = logistica().fit(treino[COLUNAS], treino["precoce"])
previsto = modelo.predict(valid[COLUNAS])
print(f"o modelo aponta {previsto.sum()} de {len(valid):,}")
y = valid["precoce"]
print(f"acurácia: {accuracy_score(y, previsto):.1%}")
print(f"revocação: {recall_score(y, previsto):.0%}")
