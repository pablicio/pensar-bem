import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import (StratifiedKFold,
                                     cross_val_score)

from risco.dados import tabela
from risco.modelos import COLUNAS, logistica

t = tabela()
X, y = t[COLUNAS], t["alvo"]
dobras = StratifiedKFold(n_splits=5, shuffle=True,
                         random_state=0)

# à mão: cada dobra é teste uma vez
aucs = []
for k, (treino, teste) in enumerate(dobras.split(X, y), 1):
    modelo = logistica().fit(X.iloc[treino], y.iloc[treino])
    p = modelo.predict_proba(X.iloc[teste])[:, 1]
    aucs.append(roc_auc_score(y.iloc[teste], p))
    taxa = y.iloc[teste].mean()
    print(f"dobra {k}: {len(teste):,} exemplos,"
          f" taxa {taxa:.3f}, AUC {aucs[-1]:.3f}")
media, desvio = np.mean(aucs), np.std(aucs)
print(f"à mão:        {media:.3f} ± {desvio:.3f}")

pronto = cross_val_score(logistica(), X, y, cv=dobras,
                         scoring="roc_auc")
media, desvio = pronto.mean(), pronto.std()
print(f"scikit-learn: {media:.3f} ± {desvio:.3f}")
