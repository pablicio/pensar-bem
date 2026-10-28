import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from finalidades import rotuladas

t = rotuladas()
palavras = CountVectorizer(strip_accents="unicode")
X = palavras.fit_transform(t["finalidade"]).toarray()
y = t["finalidade_categoria"].to_numpy()
classes = np.unique(y)
print(f"{len(t)} frases, {X.shape[1]} palavras diferentes")

# à mão: a priori de cada classe e as contagens com Laplace
log_priori = np.log([np.mean(y == c) for c in classes])
contagem = np.array([X[y == c].sum(axis=0) for c in classes])
suave = contagem + 1                       # Laplace: soma 1
log_palavra = np.log(suave / suave.sum(axis=1, keepdims=True))


def a_mao(frases):
    x = palavras.transform(frases).toarray()
    log_post = x @ log_palavra.T + log_priori
    log_post -= log_post.max(axis=1, keepdims=True)
    p = np.exp(log_post)
    return p / p.sum(axis=1, keepdims=True)


nb = MultinomialNB(alpha=1.0).fit(X, y)
novas = ["pra rodar o negocio", "ACERTAR COM O AGIOTA",
         "comprar tecido e quitar uma conta"]
print("classes:", ", ".join(c.split()[-1] for c in classes))
pelo_sklearn = nb.predict_proba(palavras.transform(novas))
for frase, m, s in zip(novas, a_mao(novas), pelo_sklearn):
    print(f"{frase}")
    print("  à mão:  ", " ".join(f"{v:.3f}" for v in m))
    print("  sklearn:", " ".join(f"{v:.3f}" for v in s))
