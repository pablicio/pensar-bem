"""A convolução escrita à mão, em NumPy."""
import numpy as np


def correlaciona(x, k):
    """Desliza o núcleo k sobre a imagem x, sem sair dela."""
    a, b = k.shape
    altura = x.shape[0] - a + 1
    largura = x.shape[1] - b + 1
    y = np.zeros((altura, largura))
    for i in range(altura):
        for j in range(largura):
            janela = x[i:i + a, j:j + b]
            y[i, j] = (janela * k).sum()     # produto escalar
    return y


def convolui(x, k):
    """A convolução da matemática: o núcleo virado."""
    return correlaciona(x, k[::-1, ::-1])
