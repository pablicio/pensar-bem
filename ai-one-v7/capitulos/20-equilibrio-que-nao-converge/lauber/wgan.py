"""O jogo da DCGAN e o de Wasserstein, num laço só, e uma
régua que não depende de nenhuma das redes."""
import torch
from torch import nn
from torch.nn.functional import logsigmoid

from lauber.dcgan import CODIGO, desenha


class Critico(nn.Module):
    """O perito da DCGAN sem normalização por lote: a nota de
    uma estampa não pode depender das outras do lote."""

    def __init__(self, c=32):
        super().__init__()
        self.corpo = nn.Sequential(
            nn.Conv2d(3, c, 4, 2, 1), nn.LeakyReLU(0.2),
            nn.Conv2d(c, 2 * c, 4, 2, 1), nn.LeakyReLU(0.2),
            nn.Conv2d(2 * c, 4 * c, 4, 2, 1),
            nn.LeakyReLU(0.2),
            nn.Flatten(), nn.Linear(4 * c * 4 * 4, 1))

    def forward(self, x):
        return self.corpo(x)


def penalidade(critico, real, falsa):
    """A média de (|gradiente da nota| - 1)², em pontos
    sorteados entre estampas reais e falsas."""
    a = torch.rand(len(real), 1, 1, 1)
    meio = (a * real + (1 - a) * falsa).requires_grad_(True)
    grad, = torch.autograd.grad(critico(meio).sum(), meio,
                                create_graph=True)
    return ((grad.flatten(1).norm(dim=1) - 1) ** 2).mean()


def fatiada(a, b, direcoes=128, semente=5):
    """A distância de Wasserstein fatiada entre dois lotes do
    mesmo tamanho: a do capítulo 16, em várias direções."""
    sorteio = torch.Generator().manual_seed(semente)
    d = torch.randn(a[0].numel(), direcoes, generator=sorteio)
    d = d / d.norm(dim=0)
    pa = (a.flatten(1) @ d).sort(dim=0).values
    pb = (b.flatten(1) @ d).sort(dim=0).values
    return float((pa - pb).abs().mean())


def treina(gerador, perito, imgs, epocas, jogo="dcgan",
           lote=64, fixo=None, criticos=5, peso=10.0):
    """jogo="dcgan": a perda do capítulo 19. jogo="wgan": a
    de Wasserstein com penalidade, um passo do gerador a cada
    `criticos` passos do crítico. Devolve as estampas do
    ruído `fixo` e, por época, a perda média do perito (na
    wgan, a estimativa da distância) e a do gerador."""
    if jogo == "dcgan":
        adam = dict(lr=2e-4, betas=(0.5, 0.999))
    else:
        adam = dict(lr=1e-4, betas=(0.0, 0.9))
    otimo_g = torch.optim.Adam(gerador.parameters(), **adam)
    otimo_p = torch.optim.Adam(perito.parameters(), **adam)
    x = imgs * 2 - 1
    fotos, historico = [], []
    for _ in range(epocas):
        anota_p, anota_g = [], []
        lotes = torch.randperm(len(x)).split(lote)
        for k, j in enumerate(lotes):
            real = x[j]
            falsa = gerador(torch.randn(len(j), CODIGO))
            nota_r = perito(real)
            nota_f = perito(falsa.detach())
            if jogo == "dcgan":
                perda_p = -(logsigmoid(nota_r).mean()
                            + logsigmoid(-nota_f).mean())
                anota_p.append(perda_p.item())
            else:
                distancia = nota_r.mean() - nota_f.mean()
                gp = penalidade(perito, real, falsa.detach())
                perda_p = -distancia + peso * gp
                anota_p.append(distancia.item())
            otimo_p.zero_grad()
            perda_p.backward()
            otimo_p.step()
            if jogo == "wgan" and k % criticos:
                continue
            nota = perito(falsa)
            if jogo == "dcgan":
                perda_g = -logsigmoid(nota).mean()
            else:
                perda_g = -nota.mean()
            otimo_g.zero_grad()
            perda_g.backward()
            otimo_g.step()
            anota_g.append(perda_g.item())
        historico.append((sum(anota_p) / len(anota_p),
                          sum(anota_g) / len(anota_g)))
        if fixo is not None:
            fotos.append(desenha(gerador, fixo))
    return fotos, historico
