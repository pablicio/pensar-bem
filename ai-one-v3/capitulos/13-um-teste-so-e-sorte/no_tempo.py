from sklearn.metrics import roc_auc_score
from sklearn.model_selection import TimeSeriesSplit

from risco.dados import tabela
from risco.modelos import COLUNAS, logistica

t = tabela().sort_values("data_concessao")
t = t.reset_index(drop=True)
X, y, data = t[COLUNAS], t["alvo"], t["data_concessao"]

print("treino até   teste de      até         AUC")
aucs = []
for treino, teste in TimeSeriesSplit(n_splits=5).split(X):
    modelo = logistica().fit(X.iloc[treino], y.iloc[treino])
    p = modelo.predict_proba(X.iloc[teste])[:, 1]
    aucs.append(roc_auc_score(y.iloc[teste], p))
    fim = data.iloc[treino[-1]].date()
    ini = data.iloc[teste[0]].date()
    ate = data.iloc[teste[-1]].date()
    print(f"{fim}   {ini}   {ate}   {aucs[-1]:.3f}")
media = sum(aucs) / len(aucs)
print(f"média {media:.3f},"
      f" de {min(aucs):.3f} a {max(aucs):.3f}")
