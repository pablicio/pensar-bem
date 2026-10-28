from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from risco.dados import tabela
from risco.modelos import COLUNAS, logistica

t = tabela()
aucs = []
for semente in range(10):
    X_tr, X_te, y_tr, y_te = train_test_split(
        t[COLUNAS], t["alvo"], test_size=0.25,
        random_state=semente, stratify=t["alvo"])
    modelo = logistica().fit(X_tr, y_tr)
    p = modelo.predict_proba(X_te)[:, 1]
    aucs.append(roc_auc_score(y_te, p))
print(" ".join(f"{a:.3f}" for a in aucs))
print(f"de {min(aucs):.3f} a {max(aucs):.3f}")
