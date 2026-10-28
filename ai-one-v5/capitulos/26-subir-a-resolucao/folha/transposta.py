"""A convolução com passo como matriz, e a sua transposta."""
from itertools import product

import numpy as np

from folha.convolucao import tamanho_saida


def toeplitz_passo(nucleo, n, passo):
    """A matriz T de y = T · x para uma convolução (correlação)
    com passo, sem preenchimento, numa imagem n × n."""
    k = nucleo.shape[0]
    m = tamanho_saida(n, k, passo)
    T = np.zeros((m * m, n * n))
    saida = product(range(m), repeat=2)
    for linha, (i, j) in enumerate(saida):
        for a, b in product(range(k), repeat=2):
            T[linha, (i * passo + a) * n + (j * passo + b)] = \
                nucleo[a, b]
    return T


def tamanho_transposta(m, k, passo, preenche=0, extra=0):
    """O lado da saída da convolução transposta."""
    return (m - 1) * passo - 2 * preenche + k + extra
