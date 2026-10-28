import matplotlib.pyplot as plt
import torch
from torch import nn

from lauber.gan import (PETALAS, petalas, rede, rosacea,
                        treina_gan)


class PeritoDoLote(nn.Module):
    """O perito recebe, além do ponto, o desvio do lote
    inteiro: falsas todas iguais ficam fáceis de achar."""

    def __init__(self):
        super().__init__()
        self.rede = rede(3, 1)

    def forward(self, x):
        desvio = x.std(dim=0).mean().expand(len(x), 1)
        return self.rede(torch.cat([x, desvio], dim=1))


FOTOS = range(0, 6001, 1000)
NA_FIGURA = (1000, 2000, 4000, 6000)
real = rosacea(2000)
print(f"rosácea de verdade: desvio {real.std(0).mean():.2f}")
fig, eixos = plt.subplots(2, 4, figsize=(10, 5))
for linha, nome in zip(eixos, ("comum", "do lote")):
    torch.manual_seed(0)
    gerador = rede(8, 2)              # oito números de ruído
    perito = rede(2, 1) if nome == "comum" else PeritoDoLote()
    fotos = treina_gan(gerador, perito, rosacea, 6000,
                       codigo=8, fotos=FOTOS)
    print(f"\nperito {nome}\npasso  pétalas  fora  desvio")
    eixos_do_passo = dict(zip(NA_FIGURA, linha))
    for passo in FOTOS:
        x = fotos[passo][0]
        conta, fora = petalas(x)
        cheias = int((conta > 20).sum())
        print(f"{passo:5d} {cheias:6d} {fora:6.0%}"
              f" {x.std(0).mean():6.2f}")
        if passo not in eixos_do_passo:
            continue
        eixo = eixos_do_passo[passo]
        eixo.scatter(*x.T, s=1, alpha=0.3, color="C3")
        eixo.scatter(*PETALAS.T, s=30, marker="+", color="k")
        eixo.set_title(f"perito {nome}, passo {passo}",
                       fontsize=8)
        eixo.set_xlim(-3.5, 3.5)
        eixo.set_ylim(-3.5, 3.5)
        eixo.set_aspect("equal")
fig.tight_layout()
fig.savefig("colapso.png", dpi=300)
