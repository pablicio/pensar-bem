import copy

import matplotlib.pyplot as plt
import torch

from lauber.gan import (PETALAS, perda_do_gerador, petalas,
                        rede, rosacea, treina_gan)

PERDAS = ("minimax", "nao_saturante")
torch.manual_seed(0)
gerador, perito = rede(2, 2), rede(2, 1)
# o perito treina sozinho por mil passos: ele "chega sabendo"
treina_gan(gerador, perito, rosacea, 1000, so_perito=1000)
z = torch.randn(256, 2)
nota = perito(gerador(z))
print(f"D(falsa) depois do perito sozinho:"
      f" {nota.sigmoid().mean():.6f}")
for perda in PERDAS:
    gerador.zero_grad()
    perda_do_gerador(perito(gerador(z)), perda).backward()
    norma = sum(p.grad.norm() ** 2
                for p in gerador.parameters()) ** 0.5
    print(f"gradiente no gerador, {perda}: {norma:.6f}")

inicio = copy.deepcopy((gerador, perito))
fig, eixos = plt.subplots(2, 4, figsize=(10, 5))
for linha, perda, lado in zip(eixos, PERDAS, (35, 3.5)):
    gerador, perito = copy.deepcopy(inicio)
    torch.manual_seed(1)
    fotos = treina_gan(gerador, perito, rosacea, 3000,
                       perda=perda, fotos=(0, 500, 1000, 3000))
    print(f"\n{perda}")
    print("passo  pétalas  fora  raio  D(real)  D(falsa)")
    for eixo, passo in zip(linha, fotos):
        x, d_r, d_f = fotos[passo]
        conta, fora = petalas(x)
        cheias = int((conta > 20).sum())
        raio = x.norm(dim=1).mean()
        print(f"{passo:5d} {cheias:6d} {fora:6.0%} {raio:5.1f}"
              f" {d_r:8.2f} {d_f:9.4f}")
        eixo.scatter(*x.T, s=1, alpha=0.3, color="C3")
        eixo.scatter(*PETALAS.T, s=30, marker="+", color="k")
        eixo.set_title(f"{perda}, passo {passo}", fontsize=8)
        eixo.set_xlim(-lado, lado)
        eixo.set_ylim(-lado, lado)
        eixo.set_aspect("equal")
fig.tight_layout()
fig.savefig("perdas.png", dpi=300)
