"""Restaurar escaneamentos: pares de treino e duas medidas."""
import numpy as np
import torch
import torch.nn.functional as F
from torch import nn

from dados.gerar_acervo import danifica


def pares(imgs, sorteio):
    """Estampas sem dano e as mesmas com um dano sorteado."""
    sujas = []
    for img in imgs.permute(0, 2, 3, 1).numpy():
        suja, _ = danifica(sorteio, img)
        sujas.append(torch.tensor(suja, dtype=torch.float32))
    return torch.stack(sujas).permute(0, 3, 1, 2), imgs


class Corretor(nn.Module):
    """Convoluções dilatadas que calculam só a correção."""

    def __init__(self, canais=32):
        super().__init__()
        camadas, entrada = [], 3
        for d in (1, 2, 4, 8, 1):
            conv = nn.Conv2d(entrada, canais, 3, padding=d,
                             dilation=d)
            camadas += [conv, nn.ReLU()]
            entrada = canais
        camadas.append(nn.Conv2d(canais, 3, 3, padding=1))
        self.rede = nn.Sequential(*camadas)

    def forward(self, x):
        return (x + self.rede(x)).clamp(0, 1)


def psnr(a, b):
    """Em decibéis, para imagens de 0 a 1: (N,)."""
    eqm = ((a - b) ** 2).mean(dim=(1, 2, 3))
    return 10 * torch.log10(1 / eqm)


def ssim(a, b, janela=7):
    """A semelhança estrutural média, em janelas de 7 x 7."""
    def media(x):
        return F.avg_pool2d(x, janela, stride=1)
    ma, mb = media(a), media(b)
    va = media(a * a) - ma ** 2
    vb = media(b * b) - mb ** 2
    cov = media(a * b) - ma * mb
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    s = ((2 * ma * mb + c1) * (2 * cov + c2)
         / ((ma ** 2 + mb ** 2 + c1) * (va + vb + c2)))
    return s.mean(dim=(1, 2, 3))
