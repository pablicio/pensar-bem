from sklearn.metrics import roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from risco.dados import tabela, treino_validacao
from risco.modelos import NUMERICAS

treino, valid = treino_validacao(tabela())
X, y = treino[NUMERICAS], treino["alvo"]
Xv, yv = valid[NUMERICAS], valid["alvo"]
print("vizinhos  AUC na validação")
for k in [5, 25, 101, 301]:
    modelo = make_pipeline(StandardScaler(),
                           KNeighborsClassifier(n_neighbors=k))
    modelo.fit(X, y)
    auc = roc_auc_score(yv, modelo.predict_proba(Xv)[:, 1])
    print(f"{k:8} {auc:17.3f}")
sem = KNeighborsClassifier(n_neighbors=101).fit(X, y)
auc = roc_auc_score(yv, sem.predict_proba(Xv)[:, 1])
print(f"101 sem padronizar: {auc:.3f}")
