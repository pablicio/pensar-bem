from sklearn.metrics import roc_auc_score

from risco.dados import tabela, treino_validacao
from risco.modelos import CATEGORICAS, COLUNAS, logistica
from vaza import COM_ATRASO, logistica_com_atraso

treino, valid = treino_validacao(tabela())
y = valid["alvo"]
modelos = [("com dias_atraso_atual", logistica_com_atraso(),
            COM_ATRASO + CATEGORICAS),
           ("sem dias_atraso_atual", logistica(), COLUNAS)]
for nome, modelo, colunas in modelos:
    modelo.fit(treino[colunas], treino["alvo"])
    p = modelo.predict_proba(valid[colunas])[:, 1]
    print(f"{nome}: AUC {roc_auc_score(y, p):.3f}")
