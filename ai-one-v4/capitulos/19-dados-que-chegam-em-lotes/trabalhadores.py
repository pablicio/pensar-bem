import time

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset

from leitora.dados import MNIST
from leitora.recorte import caixa, como_mnist, em_branco


class RecortaNaHora(Dataset):
    """Recorta cada caixa só quando é pedida: trabalho caro."""

    def __init__(self):
        d = np.load("dados/brutos/cartoes_verao.npz")
        self.folhas = d["folhas"][:180]
        self.lista = [(n, q, k) for n in range(180)
                      for q in range(10) for k in range(3)]

    def __len__(self):
        return len(self.lista)

    def __getitem__(self, i):
        n, q, k = self.lista[i]
        tinta = caixa(self.folhas[n], q, k)
        if em_branco(tinta):
            return torch.zeros(28, 28)
        return torch.from_numpy(como_mnist(tinta))


for nome, dados in [("MNIST, já na memória", MNIST("treino")),
                    ("cartões, recortando", RecortaNaHora())]:
    for n in (0, 2):
        lotes = DataLoader(dados, batch_size=64, num_workers=n)
        inicio = time.perf_counter()
        for _ in lotes:
            pass
        s = time.perf_counter() - inicio
        print(f"{nome:22} num_workers={n}: {s:5.1f} s")
