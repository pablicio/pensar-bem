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
