"""O VAE condicional: a família entra no codificador e no
decodificador."""
import torch
from torch import nn
from torch.nn.functional import one_hot

from lauber.acervo import FAMILIAS
from lauber.vae import VAE, kl

F = len(FAMILIAS)


def rotulo(familia):
    """A família (0 a 5) como seis números, um deles 1."""
    return one_hot(familia, F).float()


class Condicional(VAE):
    """O VAE convolucional, com a família ao lado do código
    na entrada das camadas lineares."""

    def __init__(self, codigo=16):
        super().__init__(codigo, convolucional=True)
        tamanho = 64 * 8 * 8
        self.media = nn.Linear(tamanho + F, codigo)
        self.logvar = nn.Linear(tamanho + F, codigo)
        self.decodificador[0] = nn.Linear(codigo + F, tamanho)

    def codifica(self, x, familia):
        h = torch.cat([self.corpo(x), rotulo(familia)], dim=1)
        return self.media(h), self.logvar(h)

    def desenha(self, z, familia):
        return self.decodificador(
            torch.cat([z, rotulo(familia)], dim=1))

    def forward(self, x, familia):
        mu, logvar = self.codifica(x, familia)
        z = self.sorteia(mu, logvar)
        return self.desenha(z, familia), mu, logvar


def treina_condicional(modelo, imgs, familias, epocas=4,
                       beta=1.0, lote=128):
    otimo = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    for _ in range(epocas):
        for j in torch.randperm(len(imgs)).split(lote):
            saida, mu, logvar = modelo(imgs[j], familias[j])
            rec = ((saida - imgs[j]) ** 2).sum(dim=(1, 2, 3))
            perda = (rec + beta * kl(mu, logvar)).mean()
            otimo.zero_grad()
            perda.backward()
            otimo.step()
