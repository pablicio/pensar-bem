"""As fotos de dados/giradas: em pé e giradas."""
import csv
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset

from folha.conjunto import CLASSES, DESVIO, MEDIA

PASTA = Path("dados/giradas")


class Giradas(Dataset):
    """As 400 fotos de uma pasta: "em_pe" ou "girada"."""

    def __init__(self, qual, lado=128):
        tabela = PASTA / "giradas.csv"
        with open(tabela, encoding="utf-8") as f:
            self.linhas = [x for x in csv.DictReader(f)
                           if x["pasta"] == qual]
        fotos = []
        for x in self.linhas:
            nome = f"{int(x['foto']):04d}.jpg"
            img = Image.open(PASTA / qual / nome)
            img = img.resize((lado, lado), Image.BOX)
            fotos.append(np.array(img))
        self.imagens = torch.from_numpy(np.stack(fotos))
        self.imagens = self.imagens.permute(0, 3, 1, 2)
        self.rotulos = torch.tensor(
            [CLASSES.index(x["verdade"]) for x in self.linhas])
        self.media = torch.tensor(MEDIA).view(3, 1, 1)
        self.desvio = torch.tensor(DESVIO).view(3, 1, 1)

    def __len__(self):
        return len(self.rotulos)

    def __getitem__(self, i):
        x = self.imagens[i].float() / 255
        return (x - self.media) / self.desvio, self.rotulos[i]
