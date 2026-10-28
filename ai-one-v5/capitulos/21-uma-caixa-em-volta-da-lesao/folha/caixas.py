"""Caixas: formatos, interseção sobre união, as do conjunto."""
import csv
from collections import defaultdict

import numpy as np
import torch
from PIL import Image

from folha.conjunto import PASTA


def para_centro(c):
    """(x0, y0, x1, y1) → (cx, cy, largura, altura)."""
    return torch.cat([(c[..., :2] + c[..., 2:]) / 2,
                      c[..., 2:] - c[..., :2]], dim=-1)


def para_cantos(c):
    """(cx, cy, largura, altura) → (x0, y0, x1, y1)."""
    return torch.cat([c[..., :2] - c[..., 2:] / 2,
                      c[..., :2] + c[..., 2:] / 2], dim=-1)


def area(c):
    return (c[..., 2:] - c[..., :2]).clamp(min=0).prod(dim=-1)


def iou(a, b):
    """A matriz N × M das interseções sobre uniões."""
    sup = torch.max(a[:, None, :2], b[None, :, :2])  # N×M×2
    inf = torch.min(a[:, None, 2:], b[None, :, 2:])
    inter = (inf - sup).clamp(min=0).prod(dim=-1)      # N × M
    uniao = area(a)[:, None] + area(b)[None, :] - inter
    return inter / uniao


def da_mascara(foto):
    """As caixas das lesões de uma foto, tiradas da máscara."""
    nome = f"{int(foto):06d}.png"
    ids = np.array(Image.open(PASTA / "lesoes" / nome))
    caixas = []
    for k in range(1, ids.max() + 1):
        ys, xs = np.nonzero(ids == k)
        if len(xs):
            caixas.append([xs.min(), ys.min(),
                           xs.max() + 1, ys.max() + 1])
    return torch.tensor(caixas, dtype=torch.float)


def do_conjunto():
    """{foto: tensor K × 4} com as caixas do caixas.csv."""
    caixas = defaultdict(list)
    with open(PASTA / "caixas.csv", encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            cantos = ("x0", "y0", "x1", "y1")
            caixas[linha["foto"]].append(
                [float(linha[k]) for k in cantos])
    return {foto: torch.tensor(c)
            for foto, c in caixas.items()}
