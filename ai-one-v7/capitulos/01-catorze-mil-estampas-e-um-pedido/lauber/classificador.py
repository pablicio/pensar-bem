"""Uma rede pequena que diz a família de uma estampa."""
import torch
from torch import nn


class Classificador(nn.Module):
    def __init__(self, familias=6):
        super().__init__()
        self.caracteristicas = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),                       # 16 x 16
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),                       # 8 x 8
            nn.Flatten(), nn.Linear(32 * 8 * 8, 64), nn.ReLU())
        self.saida = nn.Linear(64, familias)

    def forward(self, x):
        return self.saida(self.caracteristicas(x))


def treina(rede, imgs, y, epocas=3, lote=64):
    otimo = torch.optim.Adam(rede.parameters(), lr=1e-3)
    for _ in range(epocas):
        for j in torch.randperm(len(imgs)).split(lote):
            perda = nn.functional.cross_entropy(rede(imgs[j]),
                                                y[j])
            otimo.zero_grad()
            perda.backward()
            otimo.step()


def acerto(rede, imgs, y):
    with torch.no_grad():
        certo = rede(imgs).argmax(1) == y
    return float(certo.float().mean())
