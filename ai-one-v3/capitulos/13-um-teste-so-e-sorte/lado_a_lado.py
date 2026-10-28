import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (StratifiedKFold,
                                     cross_val_score)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from risco.dados import tabela
from risco.modelos import COLUNAS, logistica

FINANCEIRAS = ["valor", "parcelas", "faturamento_declarado",
               "comprometimento", "atrasos_anteriores",
               "idade"]
t = tabela()
dobras = StratifiedKFold(n_splits=5, shuffle=True,
                         random_state=0)
simples = make_pipeline(StandardScaler(),
                        LogisticRegression(max_iter=5_000))
a = cross_val_score(logistica(), t[COLUNAS], t["alvo"],
                    cv=dobras, scoring="roc_auc")
b = cross_val_score(simples, t[FINANCEIRAS], t["alvo"],
                    cv=dobras, scoring="roc_auc")
print("dobra  completa  financeira  diferença")
for k, (x, z) in enumerate(zip(a, b), 1):
    print(f"{k:5} {x:9.3f} {z:11.3f} {x - z:10.3f}")
d = a - b
print(f"diferença média {d.mean():.3f}, menor {d.min():.3f}")
