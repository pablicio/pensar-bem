"""Softmax e perdas, do jeito que não estoura."""
import numpy as np


def log_softmax(z):
    """log da softmax, pela conta de log-soma-exp."""
    m = z.max(axis=-1, keepdims=True)
    lse = m + np.log(np.exp(z - m).sum(axis=-1, keepdims=True))
    return z - lse


def softmax(z):
    return np.exp(log_softmax(z))


def entropia_cruzada(z, rotulo):
    """−log da probabilidade que a rede dá ao rótulo certo."""
    return -log_softmax(z)[..., rotulo]


def quadratica(z, rotulo):
    """A distância ao quadrado até o rótulo."""
    alvo = np.zeros(z.shape[-1])
    alvo[rotulo] = 1
    return ((softmax(z) - alvo) ** 2).sum(axis=-1)
