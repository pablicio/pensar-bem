"""Uma representação em que folhas parecidas ficam perto."""
import numpy as np
import torch
from PIL import Image
from torch import nn

from folha.qualidade import tensores


class Projecao(nn.Module):
    """512 características → 64 números de comprimento 1."""

    def __init__(self, entrada=512, saida=64):
        super().__init__()
        self.rede = nn.Sequential(nn.Linear(entrada, 256),
                                  nn.ReLU(),
                                  nn.Linear(256, saida))

    def forward(self, f):
        return nn.functional.normalize(self.rede(f), dim=1)


def distancias(a, b):
    """A matriz N × M das distâncias euclidianas ao quadrado:
    |a|² + |b|² − 2 a·b, sem laço nenhum."""
    return ((a ** 2).sum(1)[:, None] + (b ** 2).sum(1)[None]
            - 2 * a @ b.T).clamp(min=0)


def perda_tripla(z, y):
    """Para cada âncora, o positivo mais distante e o negativo
    mais próximo do lote, com margem suave (Hermans, Beyer e
    Leibe, 2017): log(1 + exp(d(a, p) − d(a, n)))."""
    d = distancias(z, z).add(1e-12).sqrt()
    mesma = y[:, None] == y[None]
    positivo = (d * mesma).max(dim=1).values
    negativo = (d + 1e9 * mesma).min(dim=1).values
    return nn.functional.softplus(positivo - negativo).mean()


def fotos_aureolada():
    """As 60 fotos de dados/aureolada, reduzidas a 128 px."""
    fotos = []
    for n in range(1, 61):
        img = Image.open(f"dados/aureolada/{n:02d}.jpg")
        img = img.resize((128, 128), Image.BOX)
        fotos.append(np.array(img))
    return tensores(fotos)
