"""Segmentação: as máscaras, a U-Net, a perda e as medidas."""
import numpy as np
import torch
from PIL import Image
from torch import nn
from torch.utils.data import Dataset

from folha.conjunto import PASTA, Folhas

CLASSES_PIXEL = ["fundo", "folha", "lesão"]


class Mascaras(Dataset):
    """Fotos de 256 e a máscara de cada pixel: 0, 1 ou 2."""

    def __init__(self, qual):
        self.fotos = Folhas(qual, lado=256)
        mascaras = []
        for linha in self.fotos.linhas:
            nome = f"{int(linha['foto']):06d}.png"
            mascaras.append(np.array(Image.open(
                PASTA / "mascaras" / nome)))
        self.mascaras = torch.from_numpy(np.stack(mascaras))
        self.mascaras = self.mascaras.long()

    def __len__(self):
        return len(self.fotos)

    def __getitem__(self, i):
        return self.fotos[i][0], self.mascaras[i]


def dupla(entrada, saida):
    """Duas convoluções 3 × 3 com normalização e ReLU."""
    return nn.Sequential(
        nn.Conv2d(entrada, saida, 3, padding=1, bias=False),
        nn.BatchNorm2d(saida), nn.ReLU(),
        nn.Conv2d(saida, saida, 3, padding=1, bias=False),
        nn.BatchNorm2d(saida), nn.ReLU())


class UNet(nn.Module):
    """Três descidas e três subidas; com `atalhos`, cada subida
    junta (concatena) o mapa da descida de mesma resolução."""

    def __init__(self, base=16, classes=3, atalhos=True):
        super().__init__()
        c = [base, 2 * base, 4 * base, 8 * base]
        self.atalhos = atalhos
        self.desce = nn.ModuleList([dupla(3, c[0]),
                                    dupla(c[0], c[1]),
                                    dupla(c[1], c[2])])
        self.fundo = dupla(c[2], c[3])
        self.sobe = nn.ModuleList(
            [nn.ConvTranspose2d(c[i + 1], c[i], 2, stride=2)
             for i in (2, 1, 0)])
        juntos = 2 if atalhos else 1
        self.junta = nn.ModuleList(
            [dupla(juntos * c[i], c[i]) for i in (2, 1, 0)])
        self.saida = nn.Conv2d(c[0], classes, 1)

    def forward(self, x):
        guardados = []
        for camada in self.desce:
            x = camada(x)
            guardados.append(x)                # para o atalho
            x = nn.functional.max_pool2d(x, 2)
        x = self.fundo(x)
        for sobe, junta, g in zip(self.sobe, self.junta,
                                  reversed(guardados)):
            x = sobe(x)
            if self.atalhos:
                x = torch.cat([g, x], dim=1)   # lado a lado
            x = junta(x)
        return self.saida(x)                   # N × 3 × H × W


def dice_suave(notas, mascara, eps=1.0):
    """1 − Dice médio das classes, com probabilidades."""
    p = notas.softmax(dim=1)
    alvo = nn.functional.one_hot(mascara, p.shape[1])
    alvo = alvo.permute(0, 3, 1, 2).float()
    inter = (p * alvo).sum(dim=(0, 2, 3))
    soma = p.sum(dim=(0, 2, 3)) + alvo.sum(dim=(0, 2, 3))
    return 1 - ((2 * inter + eps) / (soma + eps)).mean()


def medidas(prevista, certa, classes=3):
    """Dice e IoU de cada classe, somando todos os pixels."""
    dice, iou = [], []
    for c in range(classes):
        p, a = prevista == c, certa == c
        inter = (p & a).sum().item()
        soma = p.sum().item() + a.sum().item()
        dice.append(2 * inter / soma)
        iou.append(inter / (soma - inter))
    return dice, iou
