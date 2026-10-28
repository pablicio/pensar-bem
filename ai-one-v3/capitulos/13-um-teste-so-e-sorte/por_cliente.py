from sklearn.model_selection import (StratifiedGroupKFold,
                                     cross_val_score)

from risco.dados import tabela
from risco.modelos import COLUNAS, logistica

t = tabela()
dobras = StratifiedGroupKFold(n_splits=5, shuffle=True,
                              random_state=0)
aucs = cross_val_score(logistica(), t[COLUNAS], t["alvo"],
                       cv=dobras, groups=t["cliente_id"],
                       scoring="roc_auc")
print(f"cada cliente numa dobra só: {aucs.mean():.3f}"
      f" ± {aucs.std():.3f}")
