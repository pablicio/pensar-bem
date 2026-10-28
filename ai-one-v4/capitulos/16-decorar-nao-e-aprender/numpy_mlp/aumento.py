"""Dígitos novos a partir dos velhos: um pixel para o lado."""
import numpy as np


def desloca(X, sorteio):
    """Move cada imagem até um pixel, em cada direção."""
    imagens = X.reshape(-1, 28, 28)
    saida = np.zeros_like(imagens)
    passos = sorteio.integers(-1, 2, size=(len(X), 2))
    for k, (dy, dx) in enumerate(passos):
        saida[k] = np.roll(imagens[k], (dy, dx), axis=(0, 1))
    return saida.reshape(-1, 784)
