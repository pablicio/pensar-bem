from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from finalidades import rotuladas
from risco.dados import tabela, treino_validacao
from risco.modelos import COLUNAS, logistica

r = rotuladas()
contar = CountVectorizer(strip_accents="unicode")
nb = make_pipeline(contar, MultinomialNB())
nb.fit(r["finalidade"], r["finalidade_categoria"])
t = tabela()
t["divida"] = (nb.predict(t["finalidade"]) == "pagar dívida")
treino, valid = treino_validacao(t)
grupos = {"sem a finalidade": COLUNAS,
          "com 'pagar dívida'": COLUNAS + ["divida"]}
for nome, colunas in grupos.items():
    modelo = logistica()
    if "divida" in colunas:
        modelo.set_params(prepara__remainder="passthrough")
    modelo.fit(treino[colunas], treino["alvo"])
    p = modelo.predict_proba(valid[colunas])[:, 1]
    auc = roc_auc_score(valid["alvo"], p)
    print(f"{nome:19} AUC {auc:.3f}")
