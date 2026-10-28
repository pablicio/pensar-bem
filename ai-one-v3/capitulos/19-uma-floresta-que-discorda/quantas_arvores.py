from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

from risco.dados import tabela, treino_validacao
from risco.modelos import NUMERICAS

treino, valid = treino_validacao(tabela())
print("árvores  sorteio de colunas  AUC validação")
for colunas in [None, "sqrt"]:
    for n in [1, 10, 100, 500]:
        floresta = RandomForestClassifier(
            n_estimators=n, min_samples_leaf=50,
            max_features=colunas, n_jobs=-1, random_state=0)
        floresta.fit(treino[NUMERICAS], treino["alvo"])
        nota = floresta.predict_proba(valid[NUMERICAS])[:, 1]
        auc = roc_auc_score(valid["alvo"], nota)
        nome = "todas" if colunas is None else "raiz"
        print(f"{n:7} {nome:>19} {auc:14.3f}")
