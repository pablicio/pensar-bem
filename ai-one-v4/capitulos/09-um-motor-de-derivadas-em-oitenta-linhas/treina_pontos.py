import random

import matplotlib.pyplot as plt
import numpy as np

from motor.rede import Rede
from pontos import pontos

random.seed(1)
xs, ys = pontos()
rede = Rede([2, 8, 1])
print(f"{len(rede.parametros())} parâmetros, {len(xs)} pontos")

for passo in range(1, 201):
    saidas = [rede(x) for x in xs]
    # perda: a média de (rótulo − tanh(saída))²
    perda = sum((y - s.tanh()) ** 2
                for y, s in zip(ys, saidas)) * (1 / len(xs))
    for p in rede.parametros():
        p.grad = 0.0                   # zera antes de derivar
    perda.backward()
    for p in rede.parametros():
        p.dado -= 0.2 * p.grad         # um passo de descida
    if passo % 40 == 0:
        acerto = sum((s.dado > 0) == (y > 0)
                     for s, y in zip(saidas, ys)) / len(ys)
        print(f"passo {passo:3}: perda {perda.dado:.4f},"
              f" acerto {acerto:.0%}")

# a fronteira: a saída da rede numa grade de pontos
t = np.linspace(-1, 1, 41)
nota = np.array([[rede([a, b]).dado for a in t] for b in t])
fig, ax = plt.subplots(figsize=(4, 4))
ax.contourf(t, t, nota > 0, alpha=0.3, cmap="coolwarm")
P = np.array(xs)
ax.scatter(P[:, 0], P[:, 1], c=ys, cmap="coolwarm", s=18)
ax.set_aspect("equal")
fig.tight_layout()
fig.savefig("fronteira.png", dpi=400)
