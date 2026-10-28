from sklearn.metrics import roc_auc_score
from sklearn.tree import DecisionTreeClassifier

from risco.dados import tabela, treino_validacao
from risco.modelos import NUMERICAS

treino, valid = treino_validacao(tabela())
print("profundidade  folhas  AUC treino  AUC validação")
for p in [1, 2, 3, 4, 5, 6, 8, 10, 15, None]:
    arvore = DecisionTreeClassifier(max_depth=p,
                                    random_state=0)
    arvore.fit(treino[NUMERICAS], treino["alvo"])
    auc = []
    for t in [treino, valid]:
        nota = arvore.predict_proba(t[NUMERICAS])[:, 1]
        auc.append(roc_auc_score(t["alvo"], nota))
    nome = str(p or "sem limite")
    print(f"{nome:>12} {arvore.get_n_leaves():7,}"
          f" {auc[0]:11.3f} {auc[1]:14.3f}")
