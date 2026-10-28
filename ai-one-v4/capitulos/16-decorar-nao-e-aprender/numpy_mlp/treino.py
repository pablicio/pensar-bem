"""O laço de treino em mini-lotes, e a avaliação."""
import numpy as np

from numpy_mlp.camadas import softmax_entropia


def avaliar(rede, X, y, lote=1_000):
    """A perda média e o acerto, sem mexer em nada."""
    perdas, acertos = [], 0
    for k in range(0, len(X), lote):
        Z = rede.frente(X[k:k + lote])
        p, _ = softmax_entropia(Z, y[k:k + lote])
        perdas.append(p * len(Z))
        acertos += (Z.argmax(axis=1) == y[k:k + lote]).sum()
    return sum(perdas) / len(X), acertos / len(X)


def uma_epoca(rede, otimizador, X, y, lote, sorteio,
              aumento=None):
    """Uma passada pelo treino, em lotes embaralhados."""
    ordem = sorteio.permutation(len(X))
    perdas = []
    for k in range(0, len(X), lote):
        i = ordem[k:k + lote]
        Xl = X[i] if aumento is None else aumento(X[i])
        p, dZ = softmax_entropia(rede.frente(Xl), y[i])
        rede.volta(dZ)
        otimizador.passo()
        perdas.append(p)
    return perdas
