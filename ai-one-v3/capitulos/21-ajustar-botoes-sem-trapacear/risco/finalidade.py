"""A finalidade escrita pelo cliente, como coluna do modelo."""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from finalidades import rotuladas


def com_divida(t):
    """Marca os pedidos cuja finalidade é pagar dívida."""
    r = rotuladas()
    contar = CountVectorizer(strip_accents="unicode")
    nb = make_pipeline(contar, MultinomialNB())
    nb.fit(r["finalidade"], r["finalidade_categoria"])
    t = t.copy()
    t["divida"] = nb.predict(t["finalidade"]) == "pagar dívida"
    return t
