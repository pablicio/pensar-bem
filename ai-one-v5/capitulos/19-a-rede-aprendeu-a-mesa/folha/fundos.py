"""Trocar o fundo das fotos, usando a máscara da folha."""
import numpy as np
import torch
from PIL import Image

from dados.camera import fundo
from folha.conjunto import PASTA, Folhas

TIPOS = ("terra", "folhagem", "mesa")


def banco(tipos, quantos, lado=128, semente=0):
    """Fundos novos do gerador, reduzidos, como tensor CHW."""
    s = np.random.default_rng(semente)
    fundos = []
    for tipo in tipos:
        for _ in range(quantos):
            img = Image.fromarray((fundo(s, tipo) * 255)
                                  .astype(np.uint8))
            fundos.append(np.array(img.resize((lado, lado),
                                              Image.BOX)))
    fundos = torch.from_numpy(np.stack(fundos))
    return fundos.permute(0, 3, 1, 2)


class FundoTrocado(Folhas):
    """Fotos com a folha recortada sobre um fundo do banco.

    Com `tipo`, cada foto ganha um fundo fixo daquele tipo; sem
    ele, um fundo sorteado a cada vez que a foto é pedida."""

    def __init__(self, qual, tipo=None, lado=128,
                 transforma=None):
        super().__init__(qual, lado, transforma=transforma)
        mascaras = []
        for linha in self.linhas:
            nome = f"{int(linha['foto']):06d}.png"
            m = Image.open(PASTA / "mascaras" / nome)
            m = m.resize((lado, lado), Image.NEAREST)
            mascaras.append(np.array(m) > 0)
        self.folha = torch.from_numpy(np.stack(mascaras))
        self.folha = self.folha[:, None]          # N×1×H×W
        self.tipo = tipo
        tipos = [tipo] if tipo else TIPOS
        self.fundos = banco(tipos, 40, lado)

    def __getitem__(self, i):
        if self.tipo:
            k = i % len(self.fundos)
        else:
            k = torch.randint(len(self.fundos), ()).item()
        img = torch.where(self.folha[i], self.imagens[i],
                          self.fundos[k])
        x = img.float() / 255
        if self.transforma:
            x = self.transforma(x)
        return (x - self.media) / self.desvio, self.rotulos[i]
