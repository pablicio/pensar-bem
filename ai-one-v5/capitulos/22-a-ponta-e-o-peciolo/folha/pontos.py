"""Pontos de referência: a ponta e o pecíolo da folha."""
import csv
import math

import numpy as np
import torch
from PIL import Image
from torch import nn
from torch.utils.data import Dataset
from torchvision.transforms import v2

from folha.conjunto import DESVIO, MEDIA, Folhas
from folha.redes import bloco_pool

CENTRO = 63.5                     # o centro da foto de 128


def gira_pontos(p, graus):
    """Os pontos p (K × 2, em pixels) girados como a rotate
    da torchvision gira a foto: anti-horário, pelo centro."""
    a = math.radians(graus)
    R = torch.tensor([[math.cos(a), math.sin(a)],
                      [-math.sin(a), math.cos(a)]])
    return (p - CENTRO) @ R.T + CENTRO


def angulo(p):
    """Graus do vetor pecíolo → ponta; 0 é a folha em pé."""
    v = p[..., 0, :] - p[..., 1, :]
    return torch.rad2deg(torch.atan2(v[..., 0], -v[..., 1]))


class Pontos(Dataset):
    """Fotos e pontos (2 × 2, em frações do lado); com `gira`,
    foto e pontos giram juntos de um ângulo sorteado."""

    def __init__(self, qual, gira=False):
        self.fotos = Folhas(qual)
        self.pontos = torch.tensor(
            [[[float(f["ponta_x"]), float(f["ponta_y"])],
              [float(f["peciolo_x"]), float(f["peciolo_y"])]]
             for f in self.fotos.linhas]) / 2   # 256 → 128
        self.gira = gira

    def __len__(self):
        return len(self.fotos)

    def __getitem__(self, i):
        x, _ = self.fotos[i]
        p = self.pontos[i]
        if self.gira:
            graus = (torch.rand(()) * 360 - 180).item()
            x = v2.functional.rotate(x, graus)
            p = gira_pontos(p, graus)
        return x, p / 128


class GiradasPontos(Dataset):
    """As fotos de dados/giradas, com a ponta e o pecíolo."""

    def __init__(self, qual):
        with open("dados/giradas/giradas.csv",
                  encoding="utf-8") as f:
            linhas = [x for x in csv.DictReader(f)
                      if x["pasta"] == qual]
        fotos = []
        for x in linhas:
            nome = f"{int(x['foto']):04d}.jpg"
            img = Image.open(f"dados/giradas/{qual}/{nome}")
            img = img.resize((128, 128), Image.BOX)
            fotos.append(np.array(img))
        x = torch.from_numpy(np.stack(fotos))
        x = x.permute(0, 3, 1, 2)
        media = torch.tensor(MEDIA).view(3, 1, 1)
        desvio = torch.tensor(DESVIO).view(3, 1, 1)
        self.x = (x.float() / 255 - media) / desvio
        self.pontos = torch.tensor(
            [[[float(f["ponta_x"]), float(f["ponta_y"])],
              [float(f["peciolo_x"]), float(f["peciolo_y"])]]
             for f in linhas]) / 2
        self.verdade = [x["verdade"] for x in linhas]

    def __len__(self):
        return len(self.x)

    def __getitem__(self, i):
        return self.x[i], self.pontos[i] / 128


class Regressao(nn.Module):
    """Quatro números direto da média global."""

    def __init__(self):
        super().__init__()
        self.rede = nn.Sequential(
            *bloco_pool(3, 16), *bloco_pool(16, 32),
            *bloco_pool(32, 64), *bloco_pool(64, 64),
            nn.AdaptiveAvgPool2d(1), nn.Flatten(),
            nn.Linear(64, 4))

    def forward(self, x):
        return torch.sigmoid(self.rede(x)).view(-1, 2, 2)


def soft_argmax(mapas):
    """A posição esperada de cada mapa (N × K × h × w), em
    frações do lado: a média das coordenadas pesada pela
    softmax dos valores."""
    n, k, h, w = mapas.shape
    p = mapas.flatten(2).softmax(dim=2).view(n, k, h, w)
    xs = (torch.arange(w) + 0.5) / w           # centros
    ys = (torch.arange(h) + 0.5) / h
    x = (p.sum(dim=2) * xs).sum(dim=2)   # soma das linhas
    y = (p.sum(dim=3) * ys).sum(dim=2)   # e das colunas
    return torch.stack([x, y], dim=2)          # N × K × 2


class Mapas(nn.Module):
    """Um mapa de 16 × 16 por ponto, lido pela soft_argmax."""

    def __init__(self):
        super().__init__()
        self.rede = nn.Sequential(
            *bloco_pool(3, 16), *bloco_pool(16, 32),
            *bloco_pool(32, 64),
            nn.Conv2d(64, 64, 3, padding=1), nn.ReLU(),
            nn.Conv2d(64, 2, 1))               # 2 × 16 × 16

    def forward(self, x):
        return soft_argmax(self.rede(x))
