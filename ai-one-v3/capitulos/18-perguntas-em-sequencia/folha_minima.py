from sklearn.metrics import roc_auc_score
from sklearn.tree import DecisionTreeClassifier

from risco.dados import tabela, treino_validacao
from risco.modelos import NUMERICAS

treino, valid = treino_validacao(tabela())
print("mínimo por folha  folhas  AUC validação")
for minimo in [1, 50, 100, 200, 400, 800]:
    arvore = DecisionTreeClassifier(min_samples_leaf=minimo,
                                    random_state=0)
    arvore.fit(treino[NUMERICAS], treino["alvo"])
    nota = arvore.predict_proba(valid[NUMERICAS])[:, 1]
    auc = roc_auc_score(valid["alvo"], nota)
    folhas = arvore.get_n_leaves()
    print(f"{minimo:16} {folhas:7,} {auc:14.3f}")
