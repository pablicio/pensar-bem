import matplotlib.pyplot as plt
import numpy as np

from xor_a_mao import rede

pontos = [(0, 0), (0, 1), (1, 0), (1, 1)]
cor = {0: "tab:blue", 1: "tab:red"}
fig, (a, b) = plt.subplots(1, 2, figsize=(8, 3.8))
t = np.linspace(-0.3, 1.3, 2)
for x1, x2 in pontos:
    h1, h2, s = rede(x1, x2)
    a.scatter(x1, x2, s=120, color=cor[s], zorder=3)
    b.scatter(h1, h2, s=120, color=cor[s], zorder=3)
a.plot(t, 0.5 - t, "--", color="gray")    # a parede de h1
a.plot(t, 1.5 - t, "--", color="gray")    # a parede de h2
b.plot(t, t - 0.5, "--", color="black")   # a parede da saída
for ax, nome in [(a, "x"), (b, "h")]:
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(-0.3, 1.3)
    ax.set_xlabel(f"{nome}1")
    ax.set_ylabel(f"{nome}2")
    ax.set_aspect("equal")
a.set_title("as entradas")
b.set_title("depois da camada escondida")
fig.tight_layout()
fig.savefig("xor.png", dpi=300)
