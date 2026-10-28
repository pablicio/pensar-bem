"""O Naive Bayes do volume 3, com os tokens do capítulo 19."""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from rio.texto import CLASSES, palavras


class Bayes:
    def __init__(self, textos, classes):
        self.contagem = CountVectorizer(analyzer=palavras)
        x = self.contagem.fit_transform(textos)
        y = [CLASSES.index(c) for c in classes]
        self.modelo = MultinomialNB().fit(x, y)

    def probabilidades(self, textos):
        x = self.contagem.transform(textos)
        return self.modelo.predict_proba(x)
