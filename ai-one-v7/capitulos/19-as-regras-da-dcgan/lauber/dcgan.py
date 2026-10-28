"""A DCGAN das estampas 32 x 32, com as regras de 2016."""
import torch
from torch import nn
from torch.nn.functional import logsigmoid

CODIGO = 64


class Gerador(nn.Module):
    """Ruído (N, 64) -> estampa (N, 3, 32, 32), de -1 a 1."""

    def __init__(self, c=32):
        super().__init__()
        self.c = c
        self.entrada = nn.Linear(CODIGO, 4 * c * 4 * 4)
        self.corpo = nn.Sequential(
            nn.BatchNorm2d(4 * c), nn.ReLU(),
            nn.ConvTranspose2d(4 * c, 2 * c, 4, 2, 1),  # 8
            nn.BatchNorm2d(2 * c), nn.ReLU(),
            nn.ConvTranspose2d(2 * c, c, 4, 2, 1),      # 16
            nn.BatchNorm2d(c), nn.ReLU(),
            nn.ConvTranspose2d(c, 3, 4, 2, 1),          # 32
            nn.Tanh())

    def forward(self, z):
        x = self.entrada(z).view(-1, 4 * self.c, 4, 4)
        return self.corpo(x)


class Perito(nn.Module):
    """Estampa (N, 3, 32, 32) -> nota (N, 1)."""

    def __init__(self, c=32):
        super().__init__()
        self.corpo = nn.Sequential(
            nn.Conv2d(3, c, 4, 2, 1),                   # 16
            nn.LeakyReLU(0.2),
            nn.Conv2d(c, 2 * c, 4, 2, 1),               # 8
            nn.BatchNorm2d(2 * c), nn.LeakyReLU(0.2),
            nn.Conv2d(2 * c, 4 * c, 4, 2, 1),           # 4
            nn.BatchNorm2d(4 * c), nn.LeakyReLU(0.2),
            nn.Flatten(), nn.Linear(4 * c * 4 * 4, 1))

    def forward(self, x):
        return self.corpo(x)


def inicia(modulo):
    """Pesos iniciais sorteados de N(0; 0,02), como em 2016."""
    if isinstance(modulo, (nn.Conv2d, nn.ConvTranspose2d,
                           nn.Linear)):
        nn.init.normal_(modulo.weight, 0.0, 0.02)
        nn.init.zeros_(modulo.bias)


def desenha(gerador, z):
    """Estampas de 0 a 1, com o gerador em avaliação."""
    gerador.eval()
    with torch.no_grad():
        x = (gerador(z) + 1) / 2
    gerador.train()
    return x


def treina_dcgan(gerador, perito, imgs, epocas, lote=128,
                 fixo=None):
    """imgs de 0 a 1. Devolve, por época, as estampas que o
    gerador desenha com o ruído `fixo`."""
    adam = dict(lr=2e-4, betas=(0.5, 0.999))
    otimo_g = torch.optim.Adam(gerador.parameters(), **adam)
    otimo_p = torch.optim.Adam(perito.parameters(), **adam)
    x = imgs * 2 - 1                 # de -1 a 1, como o Tanh
    fotos = []
    for _ in range(epocas):
        for j in torch.randperm(len(x)).split(lote):
            falsa = gerador(torch.randn(len(j), CODIGO))
            perda_p = -(logsigmoid(perito(x[j])).mean()
                        + logsigmoid(-perito(falsa.detach()))
                        .mean())
            otimo_p.zero_grad()
            perda_p.backward()
            otimo_p.step()
            perda_g = -logsigmoid(perito(falsa)).mean()
            otimo_g.zero_grad()
            perda_g.backward()
            otimo_g.step()
        if fixo is not None:
            fotos.append(desenha(gerador, fixo))
    return fotos
