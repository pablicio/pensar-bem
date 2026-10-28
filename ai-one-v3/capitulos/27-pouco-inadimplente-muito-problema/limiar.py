from sklearn.metrics import precision_score, recall_score

from precoce import divisao
from risco.modelos import COLUNAS, logistica

treino, valid = divisao()
y = valid["precoce"]
modelo = logistica().fit(treino[COLUNAS], treino["precoce"])
nota = modelo.predict_proba(valid[COLUNAS])[:, 1]

print("limiar  apontados  precisão  revocação")
for limiar in [0.5, 0.10, 0.05, 0.03]:
    aponta = nota >= limiar
    prec = precision_score(y, aponta)
    rev = recall_score(y, aponta)
    n = aponta.sum()
    print(f"{limiar:6} {n:10,} {prec:9.1%} {rev:10.0%}")
