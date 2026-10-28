"""Da estampa gerada às telas da serigrafia."""
import numpy as np
from sklearn.cluster import KMeans


def para_lab(rgb):
    """RGB de 0 a 1 (..., 3) para CIELAB, com o branco D65:
    a escala em que distâncias iguais parecem diferenças de
    cor iguais."""
    c = np.where(rgb > 0.04045, ((rgb + 0.055) / 1.055) ** 2.4,
                 rgb / 12.92)
    m = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.9505, 1.0, 1.089])
    f = np.where(xyz > 0.008856, np.cbrt(xyz),
                 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16,
                     500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], axis=-1)


def delta_e(a, b):
    """A diferença de cor média (ΔE de 1976) entre duas
    imagens RGB (..., 3)."""
    return float(np.linalg.norm(para_lab(a) - para_lab(b),
                                axis=-1).mean())


def reduz(img, cores, semente=0):
    """img (H, W, 3) de 0 a 1 -> (H, W) com o número da cor de
    cada pixel e a paleta (cores, 3), escolhida pelo k-means
    no espaço Lab."""
    pixels = img.reshape(-1, 3)
    km = KMeans(cores, n_init=10, random_state=semente)
    rotulos = km.fit_predict(para_lab(pixels))
    paleta = np.array([pixels[rotulos == k].mean(axis=0)
                       for k in range(cores)])
    return rotulos.reshape(img.shape[:2]), paleta


def telas(rotulos, cores):
    """Uma máscara por cor: onde a tela deixa a tinta."""
    return np.stack([rotulos == k for k in range(cores)])


def vizinhos(rotulos):
    """Os oito vizinhos de cada pixel, dando a volta (é um
    rapport): (8, H, W)."""
    return np.stack([np.roll(rotulos, (dy, dx), axis=(0, 1))
                     for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                     if (dy, dx) != (0, 0)])


def ilhas(rotulos):
    """Pixels sem nenhum vizinho da mesma cor: pontos soltos
    que a tela não grava bem."""
    sozinhos = (vizinhos(rotulos) != rotulos).all(axis=0)
    return int(sozinhos.sum())


def limpa(rotulos, cores):
    """Cada pixel fica com a cor mais comum entre ele e os
    oito vizinhos."""
    todos = np.concatenate([rotulos[None], vizinhos(rotulos)])
    votos = np.stack([(todos == k).sum(axis=0)
                      for k in range(cores)])
    return votos.argmax(axis=0)


def tinta_mais_proxima(cor, tintas):
    """A tinta do estoque mais parecida com a cor, e o ΔE."""
    d = np.linalg.norm(para_lab(tintas) - para_lab(cor),
                       axis=1)
    return int(d.argmin()), float(d.min())
