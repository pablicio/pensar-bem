import csv

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

PASTA = "dados/brutos"
with open(f"{PASTA}/fotos.csv", encoding="utf-8") as f:
    fotos = list(csv.DictReader(f))
medias = {}
for foto in fotos:
    n = int(foto["foto"])
    img = np.array(Image.open(f"{PASTA}/fotos/{n:06d}.jpg"))
    m = np.array(Image.open(f"{PASTA}/mascaras/{n:06d}.png"))
    for nome, valor in [(foto["verdade"], 2), ("folha", 1)]:
        if (m == valor).any():
            media = img[m == valor].mean(axis=0)
            medias.setdefault(nome, []).append(media)

print(f"{'':14} {'fotos':>5}   R      G      B")
for nome, v in medias.items():
    r, g, b = np.mean(v, axis=0)
    print(f"{nome:14} {len(v):5} {r:6.1f} {g:6.1f} {b:6.1f}")

fig, ax = plt.subplots(figsize=(5, 4))
for nome, v in medias.items():
    v = np.array(v)[:300]
    ax.scatter(v[:, 0], v[:, 1], s=4, label=nome)
ax.set_xlabel("vermelho médio")
ax.set_ylabel("verde médio")
ax.legend(fontsize=7, markerscale=3)
fig.tight_layout()
fig.savefig("cores.png", dpi=300)
