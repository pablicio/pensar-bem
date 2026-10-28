from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from finalidades import rotuladas
from risco.dados import tabela

r = rotuladas()
contar = CountVectorizer(strip_accents="unicode")
modelo = make_pipeline(contar, MultinomialNB())
modelo.fit(r["finalidade"], r["finalidade_categoria"])

t = tabela()
t["finalidade_prevista"] = modelo.predict(t["finalidade"])
resumo = t.groupby("finalidade_prevista")["alvo"].agg(
    ["size", "mean"])
resumo.columns = ["empréstimos", "chegaram a 90"]
print(resumo.round(3).to_string())
