"""Estampas que emendam: a medida da costura, o ladrilho e um
gerador que pensa a estampa como um rolo."""
import torch
from torch import nn
from torch.nn.functional import logsigmoid

from lauber.dcgan import CODIGO


def costura(imgs):
    """A diferença média entre a última coluna e a primeira,
    e entre a última linha e a primeira, dividida pela mesma
    diferença entre as duas colunas e as duas linhas do meio.
    Perto de 1: a emenda não se distingue do meio."""
    h = lambda a, b: (a - b).abs().mean()
    m = imgs.shape[-1] // 2
    borda = (h(imgs[..., -1], imgs[..., 0])
             + h(imgs[..., -1, :], imgs[..., 0, :]))
    meio = (h(imgs[..., m - 1], imgs[..., m])
            + h(imgs[..., m - 1, :], imgs[..., m, :]))
    return float(borda / meio)


def ladrilho(img, vezes=3):
    """A estampa (3, H, W) repetida vezes x vezes."""
    return img.repeat(1, vezes, vezes)


def sobe(entrada, saida):
    """Dobra o tamanho e convolui, com a borda dando a volta:
    o pixel da esquerda tem como vizinho o da direita."""
    return nn.Sequential(
        nn.Upsample(scale_factor=2),
        nn.Conv2d(entrada, saida, 3, padding=1,
                  padding_mode="circular"))


class GeradorCircular(nn.Module):
    """O gerador da DCGAN com reamostragem e convolução
    circular no lugar das convoluções transpostas."""

    def __init__(self, c=32):
        super().__init__()
        self.c = c
        self.entrada = nn.Linear(CODIGO, 4 * c * 4 * 4)
        self.corpo = nn.Sequential(
            nn.BatchNorm2d(4 * c), nn.ReLU(),
            sobe(4 * c, 2 * c),                         # 8
            nn.BatchNorm2d(2 * c), nn.ReLU(),
            sobe(2 * c, c),                             # 16
            nn.BatchNorm2d(c), nn.ReLU(),
            sobe(c, 3),                                 # 32
            nn.Tanh())

    def forward(self, z):
        x = self.entrada(z).view(-1, 4 * self.c, 4, 4)
        return self.corpo(x)


def rola(x):
    """Cada estampa deslocada por um sorteio, dando a volta:
    a emenda de quem não emenda aparece no meio."""
    dy, dx = torch.randint(x.shape[-1], (2,)).tolist()
    return torch.roll(x, shifts=(dy, dx), dims=(2, 3))


def treina_emenda(gerador, perito, imgs, epocas, lote=128,
                  rolar=False):
    """O laço de `treina_dcgan`; com `rolar`, o perito vê as
    reais e as falsas deslocadas."""
    adam = dict(lr=2e-4, betas=(0.5, 0.999))
    otimo_g = torch.optim.Adam(gerador.parameters(), **adam)
    otimo_p = torch.optim.Adam(perito.parameters(), **adam)
    x = imgs * 2 - 1
    mexe = rola if rolar else (lambda lote: lote)
    for _ in range(epocas):
        for j in torch.randperm(len(x)).split(lote):
            falsa = mexe(gerador(torch.randn(len(j), CODIGO)))
            perda_p = -(logsigmoid(perito(mexe(x[j]))).mean()
                        + logsigmoid(-perito(falsa.detach()))
                        .mean())
            otimo_p.zero_grad()
            perda_p.backward()
            otimo_p.step()
            perda_g = -logsigmoid(perito(falsa)).mean()
            otimo_g.zero_grad()
            perda_g.backward()
            otimo_g.step()
