"""A ResNet-18 da ImageNet, como extratora."""
import torch
from torch import nn
from torchvision.models import ResNet18_Weights, resnet18

from folha.conjunto import DESVIO, MEDIA
from folha.treino import lotes

# as estatísticas das fotos da ImageNet, as do treino da rede
IMAGENET_MEDIA = (0.485, 0.456, 0.406)
IMAGENET_DESVIO = (0.229, 0.224, 0.225)


def canal(valores):
    return torch.tensor(valores).view(1, 3, 1, 1)


class Renormaliza(nn.Module):
    """Troca a normalização das folhas pela da ImageNet."""

    def __init__(self):
        super().__init__()
        escala = canal(DESVIO) / canal(IMAGENET_DESVIO)
        desloca = (canal(MEDIA) - canal(IMAGENET_MEDIA)) \
            / canal(IMAGENET_DESVIO)
        self.register_buffer("escala", escala)
        self.register_buffer("desloca", desloca)

    def forward(self, x):
        return x * self.escala + self.desloca


def extratora():
    """A ResNet-18 sem a camada final: foto → 512 números."""
    rede = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
    rede.fc = nn.Identity()
    return nn.Sequential(Renormaliza(), rede).eval()


@torch.no_grad()
def extrai(rede, dados):
    """A matriz de características: uma linha por foto."""
    linhas, rotulos = [], []
    for x, y in lotes(dados, 128):
        linhas.append(rede(x))
        rotulos.append(y)
    return torch.cat(linhas), torch.cat(rotulos)


def treina_cabeca(x, y, passos=300, semente=0):
    """Uma camada densa sobre as características."""
    torch.manual_seed(semente)
    cabeca = nn.Linear(x.shape[1], 6)
    otimizador = torch.optim.Adam(cabeca.parameters(), lr=1e-3)
    for _ in range(passos):
        otimizador.zero_grad()
        nn.functional.cross_entropy(cabeca(x), y).backward()
        otimizador.step()
    return cabeca
