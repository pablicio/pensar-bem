"""A máquina que juntava tudo, e a medida que a denunciou."""
import torch
from torch import nn

from lauber.dcgan import CODIGO
from lauber.emenda import GeradorCircular
from lauber.encomenda import F
from lauber.vizinhos import normaliza


class GeradorDaColecao(GeradorCircular):
    """O gerador circular do capítulo 25 com a família do
    capítulo 21 ao lado do ruído."""

    def __init__(self, c=32):
        super().__init__(c)
        self.familia = nn.Embedding(F, 16)
        self.entrada = nn.Linear(CODIGO + 16, 4 * c * 4 * 4)

    def forward(self, z, familia):
        z = torch.cat([z, self.familia(familia)], dim=1)
        return super().forward(z)


def parecenca(x):
    """A correlação média entre duas estampas quaisquer do
    lote: perto de 1, são todas a mesma."""
    a = normaliza(x)
    n = len(a)
    return float(((a @ a.T).sum() - n) / (n * n - n))
