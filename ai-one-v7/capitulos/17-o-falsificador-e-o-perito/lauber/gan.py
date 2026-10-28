"""GANs pequenas: a rosácea de oito pétalas e o treino."""
import math

import torch
from torch import nn
from torch.nn.functional import logsigmoid

PETALAS = torch.tensor([[2 * math.cos(k * math.pi / 4),
                         2 * math.sin(k * math.pi / 4)]
                        for k in range(8)])
RAIO = 0.1


def rosacea(n):
    """n pontos das oito pétalas, sorteadas por igual."""
    k = torch.randint(8, (n,))
    return PETALAS[k] + RAIO * torch.randn(n, 2)


def rede(entrada, saida, oculta=128):
    return nn.Sequential(nn.Linear(entrada, oculta), nn.ReLU(),
                         nn.Linear(oculta, oculta), nn.ReLU(),
                         nn.Linear(oculta, saida))


def petalas(amostras):
    """Quantas amostras caem perto de cada pétala, e a
    fração que não cai perto de nenhuma."""
    perto, qual = torch.cdist(amostras, PETALAS).min(dim=1)
    dentro = perto < 3 * RAIO
    conta = torch.bincount(qual[dentro], minlength=8)
    return conta, float(1 - dentro.float().mean())


def perda_do_gerador(nota, perda):
    """nota: a saída do perito, antes da sigmoide."""
    if perda == "minimax":       # minimiza log(1 - D)
        return logsigmoid(-nota).mean()
    return -logsigmoid(nota).mean()     # minimiza -log D


def treina_gan(gerador, perito, dados, passos, codigo=2,
               perda="nao_saturante", lote=256, lr=1e-3,
               so_perito=0, fotos=()):
    """Alterna um passo do perito e um do gerador; nos
    `so_perito` primeiros passos, só o perito treina. Devolve,
    para cada passo de `fotos`, 2000 amostras do gerador e as
    notas médias do perito, D(real) e D(falsa)."""
    otimo_g = torch.optim.Adam(gerador.parameters(), lr=lr)
    otimo_p = torch.optim.Adam(perito.parameters(), lr=lr)
    instantes = {}
    for passo in range(passos + 1):
        real = dados(lote)
        falsa = gerador(torch.randn(lote, codigo))
        nota_r, nota_f = perito(real), perito(falsa.detach())
        if passo in fotos:
            with torch.no_grad():
                amostras = gerador(torch.randn(2000, codigo))
                d_r = nota_r.sigmoid().mean().item()
                d_f = nota_f.sigmoid().mean().item()
            instantes[passo] = (amostras, d_r, d_f)
        if passo == passos:
            break
        # o perito: D(real) para 1, D(falsa) para 0
        perda_p = -(logsigmoid(nota_r).mean()
                    + logsigmoid(-nota_f).mean())
        otimo_p.zero_grad()
        perda_p.backward()
        otimo_p.step()
        if passo < so_perito:
            continue
        # o gerador: D(falsa) para 1
        perda_g = perda_do_gerador(perito(falsa), perda)
        otimo_g.zero_grad()
        perda_g.backward()
        otimo_g.step()
    return instantes
