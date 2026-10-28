import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import PredefinedSplit
from sklearn.model_selection import RandomizedSearchCV

from botoes import BOTOES, COL
from risco.dados import lacrar, tabela, treino_validacao
from risco.finalidade import com_divida
from risco.modelos import boosting

aberto, teste = lacrar(com_divida(tabela()))
treino, valid = treino_validacao(aberto)
# -1: só treina; 0: é a validação. Uma divisão só, no tempo.
dobra = np.where(aberto.index.isin(valid.index), 0, -1)

busca = RandomizedSearchCV(boosting(), BOTOES, n_iter=60,
                           scoring="roc_auc",
                           cv=PredefinedSplit(dobra),
                           random_state=0)
busca.fit(aberto[COL], aberto["alvo"])

for nome, valor in busca.best_params_.items():
    print(f"{nome.removeprefix('modelo__'):18} {valor:.4g}")
print(f"\nAUC na validação: {busca.best_score_:.3f}")

# a única vez que o teste é aberto
nota = busca.predict_proba(teste[COL])[:, 1]
auc = roc_auc_score(teste["alvo"], nota)
print(f"AUC no teste:     {auc:.3f}")
