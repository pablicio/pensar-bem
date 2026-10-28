import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

from risco.alvo import carteira
from risco.dados import com_variaveis, tabela, treino_validacao
from risco.modelos import NUMERICAS

treino, valid = treino_validacao(tabela())
e = carteira()
cida = com_variaveis(e[e["cliente_id"] == "C00000"].tail(1))

floresta = RandomForestClassifier(n_estimators=500,
                                  min_samples_leaf=50,
                                  oob_score=True, n_jobs=-1,
                                  random_state=0)
floresta.fit(treino[NUMERICAS], treino["alvo"])

fora = floresta.oob_decision_function_[:, 1]
nota = floresta.predict_proba(valid[NUMERICAS])[:, 1]
auc_fora = roc_auc_score(treino["alvo"], fora)
auc_valid = roc_auc_score(valid["alvo"], nota)
print(f"AUC fora da sacola: {auc_fora:.3f}")
print(f"AUC na validação:   {auc_valid:.3f}")

votos = [a.predict_proba(cida[NUMERICAS].to_numpy())[0, 1]
         for a in floresta.estimators_]
print()
print(f"Dona Cida, a floresta: {np.mean(votos):.1%}")
print(f"  as árvores: de {min(votos):.1%} a {max(votos):.1%}")
