"""Do cartão escaneado à caixa de 28 por 28 que a rede lê."""
import numpy as np
from PIL import Image

# o molde do cartão, impresso pela comissão: em pixels
CAIXA, PASSO, MARGEM_X, MARGEM_Y = 40, 48, 20, 60
BORDA = 3                    # o que se corta da caixa
TINTA_MINIMA = 20            # menos pixels que isso: em branco


def caixa(folha, questao, k):
    """O miolo de uma caixa: tinta clara em fundo zero."""
    x = MARGEM_X + k * PASSO + BORDA
    y = MARGEM_Y + questao * PASSO + BORDA
    lado = CAIXA - 2 * BORDA
    miolo = folha[y:y + lado, x:x + lado].astype(float)
    tinta = 235 - miolo          # papel 0, tinta alta
    return np.clip(tinta - 30, 0, None)   # tira o ruído


def em_branco(tinta):
    return (tinta > 60).sum() < TINTA_MINIMA


def como_mnist(tinta):
    """Cabe em 20 por 20 e centra pelo centro de massa."""
    linhas = np.where(tinta.max(axis=1) > 60)[0]
    colunas = np.where(tinta.max(axis=0) > 60)[0]
    recorte = tinta[linhas[0]:linhas[-1] + 1,
                    colunas[0]:colunas[-1] + 1]
    a, l = recorte.shape
    fator = 20 / max(a, l)
    tam = (max(1, round(l * fator)), max(1, round(a * fator)))
    img = Image.fromarray((recorte / recorte.max() * 255)
                          .astype(np.uint8))
    menor = np.asarray(img.resize(tam, Image.LANCZOS), float)
    saida = np.zeros((28, 28))
    a, l = menor.shape
    y0, x0 = (28 - a) // 2, (28 - l) // 2
    saida[y0:y0 + a, x0:x0 + l] = menor
    ys, xs = np.indices(saida.shape)
    massa = saida.sum()
    dy = round(14 - (ys * saida).sum() / massa)
    dx = round(14 - (xs * saida).sum() / massa)
    saida = np.roll(saida, (dy, dx), axis=(0, 1))
    return (saida / 255).astype(np.float32)
