"""A DCGAN condicional: a família entra no gerador e no
perito."""
import torch
from torch import nn
from torch.nn.functional import logsigmoid, one_hot

from lauber.dcgan import CODIGO, Gerador, Perito

F = 6                                  # as seis famílias


class GeradorPorFamilia(Gerador):
    """O gerador da DCGAN; a família, como um vetor aprendido
    de 16 números, entra ao lado do ruído."""

    def __init__(self, c=32):
        super().__init__(c)
        self.familia = nn.Embedding(F, 16)
        self.entrada = nn.Linear(CODIGO + 16, 4 * c * 4 * 4)

    def forward(self, z, familia):
        z = torch.cat([z, self.familia(familia)], dim=1)
        return super().forward(z)


class PeritoPorFamilia(Perito):
    """O perito da DCGAN; a família entra como seis canais a
    mais, um deles todo 1 e os outros todos 0."""

    def __init__(self, c=32):
        super().__init__(c)
        self.corpo[0] = nn.Conv2d(3 + F, c, 4, 2, 1)

    def forward(self, x, familia):
        canais = one_hot(familia, F).float()[:, :, None, None]
        canais = canais.expand(-1, -1, *x.shape[2:])
        return super().forward(torch.cat([x, canais], dim=1))


def desenha_familia(gerador, z, familia):
    gerador.eval()
    with torch.no_grad():
        x = (gerador(z, familia) + 1) / 2
    gerador.train()
    return x


def treina_por_familia(gerador, perito, imgs, familias, epocas,
                       lote=128):
    """O laço de `treina_dcgan`, com a família de cada
    estampa real e uma família sorteada para cada falsa."""
    adam = dict(lr=2e-4, betas=(0.5, 0.999))
    otimo_g = torch.optim.Adam(gerador.parameters(), **adam)
    otimo_p = torch.optim.Adam(perito.parameters(), **adam)
    x = imgs * 2 - 1
    for _ in range(epocas):
        for j in torch.randperm(len(x)).split(lote):
            pedida = familias[torch.randint(len(x), (len(j),))]
            ruido = torch.randn(len(j), CODIGO)
            falsa = gerador(ruido, pedida)
            nota_r = perito(x[j], familias[j])
            nota_f = perito(falsa.detach(), pedida)
            perda_p = -(logsigmoid(nota_r).mean()
                        + logsigmoid(-nota_f).mean())
            otimo_p.zero_grad()
            perda_p.backward()
            otimo_p.step()
            perda_g = -logsigmoid(perito(falsa, pedida)).mean()
            otimo_g.zero_grad()
            perda_g.backward()
            otimo_g.step()
