import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from finalidades import rotuladas

t = rotuladas()
contar = CountVectorizer(strip_accents="unicode")
X = contar.fit_transform(t["finalidade"])
nb = MultinomialNB().fit(X, t["finalidade_categoria"])
vocabulario = contar.get_feature_names_out()
for classe, logp in zip(nb.classes_, nb.feature_log_prob_):
    fortes = vocabulario[np.argsort(-logp)[:4]]
    print(f"{classe:16} {', '.join(fortes)}")
