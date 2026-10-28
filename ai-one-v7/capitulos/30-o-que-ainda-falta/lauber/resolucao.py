"""Estampas maiores: um acervo de 64 x 64 e uma DCGAN de
qualquer lado que seja potência de dois."""
import math

import numpy as np
import torch
from torch import nn

from dados.estampas import FAMILIAS, PALETAS, desenha
from lauber.dcgan import CODIGO


def acervo_em(lado, n, semente=0):
    """n estampas novas de lado x lado, sorteadas como as do
    acervo, sem os danos da digitalização."""
    sorteio = np.random.default_rng(semente)
    decadas = list(PALETAS)
    imgs = [desenha(sorteio, sorteio.integers(len(FAMILIAS)),
                    decadas[sorteio.integers(len(decadas))],
                    tamanho=lado) for _ in range(n)]
    return torch.tensor(np.stack(imgs)).permute(0, 3, 1, 2)


def gerador(lado, c=32):
    """A DCGAN do capítulo 19, com uma camada a mais a cada
    vez que o lado dobra."""
    passos = int(math.log2(lado // 4))
    largura = [c * 2 ** k for k in reversed(range(passos))]
    camadas = [nn.Unflatten(1, (largura[0], 4, 4)),
               nn.BatchNorm2d(largura[0]), nn.ReLU()]
    for a, b in zip(largura, largura[1:] + [3]):
        camadas.append(nn.ConvTranspose2d(a, b, 4, 2, 1))
        camadas += ([nn.BatchNorm2d(b), nn.ReLU()] if b != 3
                    else [nn.Tanh()])
    return nn.Sequential(nn.Linear(CODIGO, largura[0] * 16),
                         *camadas)


def perito(lado, c=32):
    """O perito da DCGAN, com uma camada a mais a cada vez
    que o lado dobra."""
    passos = int(math.log2(lado // 4))
    largura = [c * 2 ** k for k in range(passos)]
    camadas = []
    for a, b in zip([3] + largura, largura):
        camadas.append(nn.Conv2d(a, b, 4, 2, 1))
        if a != 3:
            camadas.append(nn.BatchNorm2d(b))
        camadas.append(nn.LeakyReLU(0.2))
    return nn.Sequential(*camadas, nn.Flatten(),
                         nn.Linear(largura[-1] * 16, 1))
