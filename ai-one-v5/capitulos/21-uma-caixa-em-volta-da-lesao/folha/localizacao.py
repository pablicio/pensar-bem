"""Uma rede que classifica a foto e regride uma caixa."""
import torch
from torch import nn
from torch.utils.data import Dataset

from folha.caixas import do_conjunto
from folha.conjunto import Folhas
from folha.redes import bloco_pool


class Lesoes(Dataset):
    """Foto, classe e uma caixa por foto, em frações do lado.

    alvo="maior": a caixa da maior lesão; alvo="uniao": a caixa
    que cobre todas as lesões da foto."""

    def __init__(self, qual, alvo):
        self.fotos = Folhas(qual)
        caixas = do_conjunto()
        alvos, quantas = [], []
        for linha in self.fotos.linhas:
            c = caixas.get(linha["foto"], torch.zeros(0, 4))
            quantas.append(len(c))
            if len(c) == 0:
                alvos.append(torch.zeros(4))
            elif alvo == "maior":
                lados = c[:, 2:] - c[:, :2]
                alvos.append(c[lados.prod(dim=1).argmax()])
            else:
                cima = c[:, :2].min(dim=0).values
                baixo = c[:, 2:].max(dim=0).values
                alvos.append(torch.cat([cima, baixo]))
        self.caixas = torch.stack(alvos) / 256
        self.quantas = torch.tensor(quantas)

    def __len__(self):
        return len(self.fotos)

    def __getitem__(self, i):
        x, y = self.fotos[i]
        return x, y, self.caixas[i], self.quantas[i] > 0


class RedeLocal(nn.Module):
    """O corpo da rede com média global e duas cabeças."""

    def __init__(self):
        super().__init__()
        self.corpo = nn.Sequential(
            *bloco_pool(3, 16), *bloco_pool(16, 32),
            *bloco_pool(32, 64), *bloco_pool(64, 64),
            nn.AdaptiveAvgPool2d(1), nn.Flatten())
        self.classe = nn.Linear(64, 6)
        self.caixa = nn.Linear(64, 4)

    def forward(self, x):
        h = self.corpo(x)
        return self.classe(h), torch.sigmoid(self.caixa(h))


def perda(saida, y, caixa, tem, peso=5.0):
    """Entropia cruzada da classe mais L1 da caixa, só nas
    fotos que têm lesão."""
    notas, prevista = saida
    classe = nn.functional.cross_entropy(notas, y)
    if not tem.any():
        return classe
    return classe + peso * nn.functional.l1_loss(prevista[tem],
                                                 caixa[tem])
