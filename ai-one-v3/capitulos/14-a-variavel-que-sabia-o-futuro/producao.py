from sklearn.metrics import roc_auc_score

from risco.dados import tabela, treino_validacao
from risco.modelos import CATEGORICAS
from vaza import COM_ATRASO, logistica_com_atraso

treino, valid = treino_validacao(tabela())
colunas = COM_ATRASO + CATEGORICAS
modelo = logistica_com_atraso().fit(treino[colunas],
                                    treino["alvo"])
# no dia do pedido, ninguém está atrasado no empréstimo novo
no_pedido = valid[colunas].assign(dias_atraso_atual=0)
p = modelo.predict_proba(no_pedido)[:, 1]
auc = roc_auc_score(valid["alvo"], p)
print(f"AUC no dia do pedido: {auc:.3f}")
print(f"probabilidade média:  {p.mean():.1%}"
      f" (real: {valid['alvo'].mean():.1%})")
print(f"maior probabilidade:  {p.max():.1%}")
