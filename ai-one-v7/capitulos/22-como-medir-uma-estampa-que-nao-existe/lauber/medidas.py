"""Medidas de um gerador, nas características do juiz."""
import numpy as np
import torch
from scipy import linalg
from scipy.spatial.distance import cdist


def caracteristicas(juiz, imgs):
    """Os 64 números da penúltima camada do juiz do capítulo
    1: o que ele olha numa estampa antes da família."""
    juiz.eval()
    with torch.no_grad():
        return juiz.caracteristicas(imgs).double().numpy()


def frechet(a, b):
    """A distância de Fréchet entre duas gaussianas ajustadas
    às características: as médias e as covariâncias."""
    ma, mb = a.mean(0), b.mean(0)
    ca, cb = np.cov(a, rowvar=False), np.cov(b, rowvar=False)
    eps = 1e-6 * np.eye(len(ma))    # sem covariância nula
    raiz = linalg.sqrtm((ca + eps) @ (cb + eps)).real
    return float(((ma - mb) ** 2).sum()
                 + np.trace(ca + cb - 2 * raiz))


def raios(x, k=3):
    """A distância de cada ponto ao seu k-ésimo vizinho."""
    return np.sort(cdist(x, x), axis=1)[:, k]


def precisao_cobertura(reais, falsas, k=3):
    """Precisão: a fração das falsas que cai na bola de
    alguma real. Cobertura: a fração das reais que cai na
    bola de alguma falsa. A bola de um ponto vai até o
    k-ésimo vizinho dele, entre os do mesmo lado."""
    d = cdist(falsas, reais)
    dentro_r = d <= raios(reais, k)[None, :]
    dentro_f = d <= raios(falsas, k)[:, None]
    return (float(dentro_r.any(axis=1).mean()),
            float(dentro_f.any(axis=0).mean()))
