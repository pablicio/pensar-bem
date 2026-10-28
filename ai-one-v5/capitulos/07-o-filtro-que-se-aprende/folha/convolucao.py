"""A convolução escrita à mão, em NumPy."""
from itertools import product

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


def tamanho_saida(n, k, passo=1, preenche=0):
    """Quantas posições o núcleo ocupa numa dimensão de n."""
    return (n + 2 * preenche - k) // passo + 1


def conv2d(x, w, b, passo=1, preenche=0):
    """Vários canais: x (C, H, W), w (S, C, k, k), b (S,)."""
    x = np.pad(x, ((0, 0), (preenche, preenche),
                   (preenche, preenche)))
    S, C, k, _ = w.shape
    altura = tamanho_saida(x.shape[1], k, passo)
    largura = tamanho_saida(x.shape[2], k, passo)
    y = np.zeros((S, altura, largura))
    for i in range(altura):
        for j in range(largura):
            lin, col = i * passo, j * passo
            janela = x[:, lin:lin + k, col:col + k]  # C×k×k
            # um produto escalar por núcleo de saída
            y[:, i, j] = (w * janela).sum(axis=(1, 2, 3)) + b
    return y


def im2col(x, k, passo=1, preenche=0):
    """Cada janela de x (C, H, W) vira uma coluna."""
    x = np.pad(x, ((0, 0), (preenche, preenche),
                   (preenche, preenche)))
    C = x.shape[0]
    altura = tamanho_saida(x.shape[1], k, passo)
    largura = tamanho_saida(x.shape[2], k, passo)
    colunas = np.zeros((C * k * k, altura * largura))
    for i in range(altura):
        for j in range(largura):
            lin, col = i * passo, j * passo
            janela = x[:, lin:lin + k, col:col + k]
            colunas[:, i * largura + j] = janela.ravel()
    return colunas, (altura, largura)


def conv2d_matricial(x, w, b, passo=1, preenche=0):
    """A mesma conv2d, como um produto de matrizes."""
    S, C, k, _ = w.shape
    colunas, (altura, largura) = im2col(x, k, passo, preenche)
    y = w.reshape(S, C * k * k) @ colunas + b[:, None]
    return y.reshape(S, altura, largura)


def toeplitz(nucleo, n):
    """A matriz T que faz y = T · x numa imagem n × n."""
    k = nucleo.shape[0]
    m = tamanho_saida(n, k)
    T = np.zeros((m * m, n * n))
    posicoes = product(range(m), repeat=2)       # saída
    for linha, (i, j) in enumerate(posicoes):
        for a, b in product(range(k), repeat=2):    # núcleo
            T[linha, (i + a) * n + (j + b)] = nucleo[a, b]
    return T


def gradientes(x, k, g):
    """dL/dk e dL/dx de Y = correlaciona(x, k); g = dL/dY."""
    d_nucleo = correlaciona(x, g)       # x passado por g
    borda = k.shape[0] - 1
    g_cheio = np.pad(g, borda)          # moldura de zeros
    d_entrada = correlaciona(g_cheio, k[::-1, ::-1])
    return d_nucleo, d_entrada
