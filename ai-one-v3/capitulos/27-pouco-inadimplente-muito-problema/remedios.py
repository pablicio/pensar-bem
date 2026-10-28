import pandas as pd
from sklearn.metrics import (average_precision_score,
                             precision_score, recall_score,
                             roc_auc_score)

from precoce import divisao
from risco.modelos import COLUNAS, logistica

treino, valid = divisao()
y = valid["precoce"]
pos = treino[treino["precoce"] == 1]
neg = treino[treino["precoce"] == 0]


def treina(t, **botoes):
    modelo = logistica().set_params(**botoes)
    return modelo.fit(t[COLUNAS], t["precoce"])


# cada remédio: um modelo treinado de um jeito diferente
copias = pos.sample(len(neg), replace=True, random_state=0)
menos = neg.sample(len(pos), random_state=0)
modelos = {
    "nada": treina(treino),
    "peso de classe": treina(treino,
                             modelo__class_weight="balanced"),
    "sobreamostragem": treina(pd.concat([neg, copias])),
    "subamostragem": treina(pd.concat([menos, pos])),
}
print("remédio            AUC    PR  média prec. revoc.")
for nome, modelo in modelos.items():
    nota = modelo.predict_proba(valid[COLUNAS])[:, 1]
    aponta = nota >= 0.5
    auc = roc_auc_score(y, nota)
    pr = average_precision_score(y, nota)
    prec = precision_score(y, aponta)
    print(f"{nome:16} {auc:5.3f} {pr:5.3f} {nota.mean():6.1%}"
          f" {prec:5.1%} {recall_score(y, aponta):5.0%}")
