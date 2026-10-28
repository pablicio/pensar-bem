"""O autoencoder variacional: nuvens, sorteio e a perda."""
import torch
from torch import nn

from lauber.convolucional import sobe


class VAE(nn.Module):
    """O codificador dá a média e o log da variância de cada
    número do código; o decodificador desenha a partir de um
    código sorteado da nuvem."""

    def __init__(self, codigo=2, convolucional=False):
        super().__init__()
        if convolucional:
            self.corpo = nn.Sequential(
                nn.Conv2d(3, 32, 3, stride=2, padding=1),
                nn.ReLU(),
                nn.Conv2d(32, 64, 3, stride=2, padding=1),
                nn.ReLU(), nn.Flatten())
            tamanho = 64 * 8 * 8
            self.decodificador = nn.Sequential(
                nn.Linear(codigo, tamanho), nn.ReLU(),
                nn.Unflatten(1, (64, 8, 8)),
                sobe(64, 32, "reamostra"), nn.ReLU(),
                sobe(32, 3, "reamostra"), nn.Sigmoid())
        else:
            self.corpo = nn.Sequential(
                nn.Flatten(), nn.Linear(3 * 32 * 32, 512),
                nn.ReLU())
            tamanho = 512
            self.decodificador = nn.Sequential(
                nn.Linear(codigo, 512), nn.ReLU(),
                nn.Linear(512, 3 * 32 * 32), nn.Sigmoid(),
                nn.Unflatten(1, (3, 32, 32)))
        self.media = nn.Linear(tamanho, codigo)
        self.logvar = nn.Linear(tamanho, codigo)

    def codifica(self, x):
        h = self.corpo(x)
        return self.media(h), self.logvar(h)

    def sorteia(self, mu, logvar):
        """A reparametrização: z = mu + sigma * epsilon."""
        epsilon = torch.randn_like(mu)
        return mu + torch.exp(0.5 * logvar) * epsilon

    def forward(self, x):
        mu, logvar = self.codifica(x)
        z = self.sorteia(mu, logvar)
        return self.decodificador(z), mu, logvar


def kl(mu, logvar):
    """KL(N(mu, sigma²) || N(0, 1)), somada no código: (N,)."""
    return 0.5 * (mu ** 2 + logvar.exp() - logvar - 1).sum(1)


def treina_vae(modelo, imgs, epocas=10, beta=1.0, lote=128,
               aquece=0):
    """Reconstrução (soma dos quadrados) + beta x KL. Com
    `aquece`, o beta cresce de 0 até o valor nessas épocas.
    Devolve, por época, a reconstrução e a KL médias."""
    otimo = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    historico = []
    for epoca in range(epocas):
        peso = beta
        if aquece:
            peso = beta * min(1.0, (epoca + 1) / aquece)
        soma_r = soma_k = 0.0
        for j in torch.randperm(len(imgs)).split(lote):
            saida, mu, logvar = modelo(imgs[j])
            rec = ((saida - imgs[j]) ** 2).sum(dim=(1, 2, 3))
            k = kl(mu, logvar)
            perda = (rec + peso * k).mean()
            otimo.zero_grad()
            perda.backward()
            otimo.step()
            soma_r += rec.sum().item()
            soma_k += k.sum().item()
        n = len(imgs)
        historico.append((soma_r / n, soma_k / n))
    return historico
