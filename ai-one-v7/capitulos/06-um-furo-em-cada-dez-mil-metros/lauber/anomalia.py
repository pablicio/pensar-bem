"""Defeitos pelo erro de reconstrução: treinar só com o bom."""
import numpy as np
import torch
import torch.nn.functional as F
from torch import nn

from lauber.convolucional import sobe

ARQUIVO = "dados/brutos/malha.npz"


def carrega_malha():
    """As fotos de malha (N, 1, 32, 32) e as informações."""
    dados = np.load(ARQUIVO)
    tensor = {k: torch.tensor(dados[k])[:, None]
              for k in ("treino", "teste")}
    info = {k: dados[k] for k in dados.files
            if k not in ("treino", "teste")}
    return tensor["treino"], tensor["teste"], info


class Malha(nn.Module):
    """O autoencoder do capítulo 4, para um canal de cinza."""

    def __init__(self, canais=4):
        super().__init__()
        self.codificador = nn.Sequential(
            nn.Conv2d(1, 32, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, canais, 3, padding=1))
        self.decodificador = nn.Sequential(
            nn.Conv2d(canais, 64, 3, padding=1), nn.ReLU(),
            sobe(64, 32, "reamostra"), nn.ReLU(),
            sobe(32, 1, "reamostra"), nn.Sigmoid())

    def forward(self, x):
        return self.decodificador(self.codificador(x))


@torch.no_grad()
def mapa_de_erro(modelo, imgs):
    """O erro quadrático de cada pixel: (N, 1, 32, 32)."""
    return (modelo(imgs) - imgs) ** 2


def escores(mapa):
    """Dois escores por foto: o erro médio e o maior erro
    local, depois de suavizar o mapa em janelas de 5 x 5."""
    media = mapa.mean(dim=(1, 2, 3))
    local = F.avg_pool2d(mapa, 5, stride=1, padding=2)
    return media, local.amax(dim=(1, 2, 3))
