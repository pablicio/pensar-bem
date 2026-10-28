"""O MNIST em vetores de 0 a 1, com a validação separada."""
import numpy as np

from mnist import carregar


def mnist_vetores():
    """Treino (50 mil), validação (10 mil) e teste (10 mil)."""
    X, y = carregar("treino")
    Xt, yt = carregar("teste")
    X = X.reshape(-1, 784).astype(np.float32) / 255
    Xt = Xt.reshape(-1, 784).astype(np.float32) / 255
    treino = (X[:50_000], y[:50_000])
    validacao = (X[50_000:], y[50_000:])
    return treino, validacao, (Xt, yt)
