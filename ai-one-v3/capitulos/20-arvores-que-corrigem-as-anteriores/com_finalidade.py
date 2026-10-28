import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from finalidades import rotuladas
from risco.dados import tabela, treino_validacao
from risco.modelos import COLUNAS, boosting

r = rotuladas()
contar = CountVectorizer(strip_accents="unicode")
nb = make_pipeline(contar, MultinomialNB())
nb.fit(r["finalidade"], r["finalidade_categoria"])
t = tabela()
t["divida"] = nb.predict(t["finalidade"]) == "pagar dívida"
colunas = COLUNAS + ["divida"]

treino, valid = treino_validacao(t)
ajuste = treino["data_concessao"] >= "2025-01-01"
antes, depois = treino[~ajuste], treino[ajuste]
modelo = boosting(iteracoes=1_500)
modelo.fit(antes[colunas], antes["alvo"])
prepara, gb = modelo.named_steps.values()
X_depois = prepara.transform(depois[colunas])
curva = [roc_auc_score(depois["alvo"], p[:, 1])
         for p in gb.staged_predict_proba(X_depois)]
melhor = int(np.argmax(curva)) + 1

final = boosting(iteracoes=melhor)
final.fit(treino[colunas], treino["alvo"])
nota = final.predict_proba(valid[colunas])[:, 1]
print(f"{melhor} árvores, AUC na validação"
      f" {roc_auc_score(valid['alvo'], nota):.3f}")
