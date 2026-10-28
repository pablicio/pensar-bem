from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import (GroupShuffleSplit,
                                     train_test_split)
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from finalidades import rotuladas

t = rotuladas()
frase, y = t["finalidade"], t["finalidade_categoria"]


def acerto(treino, teste):
    contar = CountVectorizer(strip_accents="unicode")
    modelo = make_pipeline(contar, MultinomialNB())
    modelo.fit(frase.iloc[treino], y.iloc[treino])
    previsto = modelo.predict(frase.iloc[teste])
    return (previsto == y.iloc[teste]).mean()


linhas = range(len(t))
treino, teste = train_test_split(list(linhas), test_size=0.3,
                                 random_state=0)
print(f"sorteando pedidos:        {acerto(treino, teste):.1%}")
grupos = frase.str.lower()
divisao = GroupShuffleSplit(n_splits=1, test_size=0.3,
                            random_state=0)
treino, teste = next(divisao.split(t, groups=grupos))
novas = grupos.iloc[teste].nunique()
print(f"só frases nunca vistas:   {acerto(treino, teste):.1%}"
      f"  ({novas} frases)")
