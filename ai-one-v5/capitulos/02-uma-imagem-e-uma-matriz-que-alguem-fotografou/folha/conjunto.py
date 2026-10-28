"""As fotos da Folha Clara: a tabela, a divisão e o Dataset."""
import csv
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset

PASTA = Path("dados/brutos")
CLASSES = ["sadia", "ferrugem", "cercosporiose",
           "bicho-mineiro", "phoma", "sol"]
MEDIA = (0.2497, 0.3222, 0.2781)     # de cada canal, no treino
DESVIO = (0.1302, 0.1033, 0.2348)


def tabela():
    """As linhas de fotos.csv, como dicionários."""
    with open(PASTA / "fotos.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parte(fazenda):
    """Treino, validação ou teste, por fazenda inteira."""
    ordem = np.random.default_rng(5).permutation(40) + 1
    n = int(fazenda[1:])
    if n in ordem[:8]:
        return "teste"
    if n in ordem[8:14]:
        return "validacao"
    return "treino"


def abre(foto, lado=128):
    """A foto, reduzida para lado × lado, como array HWC."""
    img = Image.open(PASTA / "fotos" / f"{int(foto):06d}.jpg")
    if lado != img.width:
        img = img.resize((lado, lado), Image.BOX)
    return np.array(img)


class Folhas(Dataset):
    """As fotos de uma parte, prontas para a rede."""

    def __init__(self, qual, lado=128, rotulo="rotulo",
                 transforma=None):
        self.linhas = [f for f in tabela()
                       if parte(f["fazenda"]) == qual]
        fotos = [abre(f["foto"], lado) for f in self.linhas]
        self.imagens = torch.from_numpy(np.stack(fotos))
        self.imagens = self.imagens.permute(0, 3, 1, 2)  # CHW
        self.rotulos = torch.tensor(
            [CLASSES.index(f[rotulo]) for f in self.linhas])
        self.transforma = transforma
        self.media = torch.tensor(MEDIA).view(3, 1, 1)
        self.desvio = torch.tensor(DESVIO).view(3, 1, 1)

    def __len__(self):
        return len(self.rotulos)

    def __getitem__(self, i):
        x = self.imagens[i].float() / 255
        if self.transforma:
            x = self.transforma(x)
        return (x - self.media) / self.desvio, self.rotulos[i]
