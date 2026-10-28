"""A ResNet pequena, agora com normalização em lote."""
import torch
from torch import nn


def conv(entrada, saida, nucleo, passo, normaliza):
    """Convolução e normalização; sem ela, a conv tem viés."""
    camada = nn.Conv2d(entrada, saida, nucleo, passo,
                       nucleo // 2, bias=not normaliza)
    if normaliza:
        return nn.Sequential(camada, nn.BatchNorm2d(saida))
    return nn.Sequential(camada, nn.Identity())


class Bloco(nn.Module):
    """O bloco residual, com ou sem normalização."""

    def __init__(self, entrada, saida, passo=1,
                 normaliza=True):
        super().__init__()
        self.c1 = conv(entrada, saida, 3, passo, normaliza)
        self.c2 = conv(saida, saida, 3, 1, normaliza)
        if entrada == saida and passo == 1:
            self.atalho = nn.Identity()
        else:                       # muda canais e resolução
            self.atalho = conv(entrada, saida, 1, passo,
                               normaliza)
        ultima = self.c2[1] if normaliza else self.c2[0]
        nn.init.zeros_(ultima.weight)   # nasce identidade
        nn.init.zeros_(ultima.bias)

    def forward(self, x):
        f = self.c2(torch.relu(self.c1(x)))
        return torch.relu(f + self.atalho(x))


def resnet_pequena(blocos=3, normaliza=True):
    """A rede do capítulo 13, com a normalização opcional."""
    camadas = [conv(3, 16, 3, 2, normaliza), nn.ReLU()]
    canais = 16
    for estagio, largura in enumerate((16, 32, 64)):
        for b in range(blocos):
            passo = 2 if b == 0 and estagio > 0 else 1
            bloco = Bloco(canais, largura, passo, normaliza)
            camadas.append(bloco)
            canais = largura
    return nn.Sequential(*camadas, nn.AdaptiveAvgPool2d(1),
                         nn.Flatten(), nn.Linear(canais, 6))
