from sklearn.metrics import roc_auc_score

from risco.dados import tabela, treino_validacao
from risco.modelos import NUMERICAS

treino, valid = treino_validacao(tabela())
suspeitas = NUMERICAS + ["dias_atraso_atual", "saldo_devedor"]
notas = {}
for coluna in suspeitas:
    auc = roc_auc_score(treino["alvo"], treino[coluna])
    notas[coluna] = max(auc, 1 - auc)
print("coluna                  AUC sozinha")
for coluna, auc in sorted(notas.items(), key=lambda x: -x[1]):
    print(f"{coluna:23} {auc:11.3f}")
