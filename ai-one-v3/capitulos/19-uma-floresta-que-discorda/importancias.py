import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance

from risco.dados import tabela, treino_validacao
from risco.modelos import NUMERICAS

t = tabela()
# o telefone como número: (71) 3375-2210 vira 33752210
digitos = t["telefone_referencia"].str.replace(r"\D", "",
                                                regex=True)
t["telefone"] = digitos.str[2:].astype(int)
COLUNAS = NUMERICAS + ["telefone"]
treino, valid = treino_validacao(t)

floresta = RandomForestClassifier(n_estimators=500,
                                  min_samples_leaf=5,
                                  n_jobs=-1, random_state=0)
floresta.fit(treino[COLUNAS], treino["alvo"])
impureza = pd.Series(floresta.feature_importances_, COLUNAS)

r = permutation_importance(floresta, valid[COLUNAS],
                           valid["alvo"], scoring="roc_auc",
                           n_repeats=5, n_jobs=-1,
                           random_state=0)
perda = pd.Series(r.importances_mean, COLUNAS)

lista = pd.DataFrame({
    "impureza": impureza.rank(ascending=False).astype(int),
    "permutação": perda.rank(ascending=False).astype(int),
    "perda de AUC": perda.round(4)})
print(lista.sort_values("impureza").to_string())
