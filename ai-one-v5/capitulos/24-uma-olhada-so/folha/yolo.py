"""Um detector de um estágio no estilo YOLO, do zero."""
import csv
from collections import defaultdict

import torch
from torch import nn
from torch.utils.data import Dataset

from folha.conjunto import PASTA, Folhas
from folha.deteccao import nms

TIPOS = ["ferrugem", "cercosporiose", "bicho-mineiro", "phoma",
         "sol"]
S, CELULA = 16, 16           # grade 16 × 16 na foto de 256


def caixas_com_tipo():
    """{foto: tensor K × 5}: cantos e o número do tipo."""
    caixas = defaultdict(list)
    with open(PASTA / "caixas.csv", encoding="utf-8") as f:
        for x in csv.DictReader(f):
            cantos = [float(x[k]) for k in ("x0", "y0", "x1",
                                            "y1")]
            tipo = TIPOS.index(x["tipo"])
            caixas[x["foto"]].append(cantos + [tipo])
    return {foto: torch.tensor(c)
            for foto, c in caixas.items()}


def iou_formas(wh, centros):
    """IoU entre formas (largura, altura) de mesmo centro:
    a matriz N × K."""
    inter = torch.min(wh[:, None], centros[None]).prod(dim=2)
    uniao = (wh.prod(dim=1)[:, None] + centros.prod(dim=1)
             - inter)
    return inter / uniao


def kmeans(wh, k, passos=50, semente=0):
    """Âncoras: k-means das formas com distância 1 − IoU."""
    sorteador = torch.Generator().manual_seed(semente)
    ordem = torch.randperm(len(wh), generator=sorteador)
    centros = wh[ordem[:k]].clone()
    for _ in range(passos):
        grupo = (1 - iou_formas(wh, centros)).argmin(dim=1)
        novos = []
        for j in range(k):     # grupo vazio: fica onde está
            membros = wh[grupo == j]
            novos.append(membros.median(dim=0).values
                         if len(membros) else centros[j])
        centros = torch.stack(novos)
    return centros[centros.prod(dim=1).argsort()]


class Grade(Dataset):
    """Fotos de 256 e o alvo de cada âncora de cada célula:
    objeto, tx, ty, tl, th e o tipo (−1 onde não há lesão)."""

    def __init__(self, qual, ancoras):
        self.fotos = Folhas(qual, lado=256)
        todas = caixas_com_tipo()
        self.caixas, self.alvos = [], []
        for linha in self.fotos.linhas:
            c = todas.get(linha["foto"], torch.zeros(0, 5))
            alvo = torch.zeros(len(ancoras), 6, S, S)
            alvo[:, 5] = -1
            for x0, y0, x1, y1, tipo in c.tolist():
                cx, cy, l, h = (x0 + x1) / 2, (y0 + y1) / 2, \
                    x1 - x0, y1 - y0
                j, i = int(cx // CELULA), int(cy // CELULA)
                forma = torch.tensor([[l, h]])
                a = iou_formas(forma, ancoras)[0].argmax()
                alvo[a, :, i, j] = torch.tensor([
                    1.0, cx / CELULA - j, cy / CELULA - i,
                    torch.log(l / ancoras[a, 0]).item(),
                    torch.log(h / ancoras[a, 1]).item(), tipo])
            self.caixas.append(c)
            self.alvos.append(alvo)

    def __len__(self):
        return len(self.fotos)

    def __getitem__(self, i):
        return self.fotos[i][0], self.alvos[i]


def bloco(entrada, saida):
    return [nn.Conv2d(entrada, saida, 3, padding=1,
                      bias=False),
            nn.BatchNorm2d(saida), nn.LeakyReLU(0.1)]


class MiniYolo(nn.Module):
    """Quatro reduções de 2: a foto de 256 vira a grade 16."""

    def __init__(self, ancoras, tipos=5):
        super().__init__()
        self.A, self.C = len(ancoras), tipos
        self.register_buffer("ancoras", ancoras)
        self.corpo = nn.Sequential(
            *bloco(3, 16), nn.MaxPool2d(2),
            *bloco(16, 32), nn.MaxPool2d(2),
            *bloco(32, 64), nn.MaxPool2d(2),
            *bloco(64, 128), nn.MaxPool2d(2),
            *bloco(128, 128),
            nn.Conv2d(128, self.A * (5 + tipos), 1))

    def forward(self, x):
        y = self.corpo(x)            # N × A·(5+C) × S × S
        return y.view(len(x), self.A, 5 + self.C, S, S)


def perda(y, alvo, peso_caixa=5.0):
    """As três partes: objeto (todas as âncoras), caixa e tipo
    (só as responsáveis por uma lesão)."""
    tem = alvo[:, :, 0] > 0                  # N × A × S × S
    objeto = nn.functional.binary_cross_entropy_with_logits(
        y[:, :, 0], alvo[:, :, 0], reduction="sum")
    yp = y.permute(0, 1, 3, 4, 2)[tem]            # R × (5 + C)
    ap = alvo.permute(0, 1, 3, 4, 2)[tem]         # R × 6
    centro = (torch.sigmoid(yp[:, 1:3]) - ap[:, 1:3]) ** 2
    tamanho = (yp[:, 3:5] - ap[:, 3:5]) ** 2
    tipo = nn.functional.cross_entropy(
        yp[:, 5:], ap[:, 5].long(), reduction="sum")
    caixa = centro.sum() + tamanho.sum()
    return (objeto + peso_caixa * caixa + tipo) / len(y)


def decodifica(y, ancoras, limiar):
    """Caixas, notas e tipos de uma foto; y: A×(5+C)×S×S."""
    objeto = torch.sigmoid(y[:, 0])
    a, i, j = (objeto > limiar).nonzero(as_tuple=True)
    t = y[a, 1:5, i, j]
    cx = (j + torch.sigmoid(t[:, 0])) * CELULA
    cy = (i + torch.sigmoid(t[:, 1])) * CELULA
    l = ancoras[a, 0] * t[:, 2].exp()
    h = ancoras[a, 1] * t[:, 3].exp()
    probs = y[a, 5:, i, j].softmax(dim=1)
    p_tipo, tipo = probs.max(dim=1)
    caixas = torch.stack([cx - l / 2, cy - h / 2,
                          cx + l / 2, cy + h / 2], dim=1)
    return caixas, objeto[a, i, j] * p_tipo, tipo


def detecta(rede, x, limiar=0.01, limiar_nms=0.3):
    """Detecções de uma foto, com NMS separada por tipo."""
    with torch.no_grad():
        y = rede(x[None])[0]
    caixas, notas, tipos = decodifica(y, rede.ancoras, limiar)
    guardadas = []
    for t in tipos.unique():
        quais = (tipos == t).nonzero().flatten()
        guardadas.append(quais[nms(caixas[quais], notas[quais],
                                   limiar_nms)])
    if guardadas:
        k = torch.cat(guardadas)
        return caixas[k], notas[k], tipos[k]
    return caixas, notas, tipos
