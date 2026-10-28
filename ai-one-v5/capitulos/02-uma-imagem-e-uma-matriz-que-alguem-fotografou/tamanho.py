import csv

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

with open("dados/brutos/caixas.csv", encoding="utf-8") as f:
    caixas = list(csv.DictReader(f))
larg = np.array([min(int(c["x1"]) - int(c["x0"]),
                     int(c["y1"]) - int(c["y0"]))
                 for c in caixas])
print(f"{len(larg)} lesões; menor lado da caixa, em pixels:")
for lado in (256, 128, 64, 32):
    k = larg * lado / 256
    print(f"  foto de {lado:3}: mediana {np.median(k):5.1f},"
          f" menores que 3 pixels: {(k < 3).mean():6.1%}")

foto = Image.open("dados/brutos/fotos/000011.jpg")
fig, eixos = plt.subplots(1, 4, figsize=(9, 2.6))
eixos[0].imshow(foto)
eixos[0].set_title("256 × 256")
metodos = [("vizinho", Image.NEAREST),
           ("bilinear", Image.BILINEAR),
           ("média (BOX)", Image.BOX)]
for ax, (nome, metodo) in zip(eixos[1:], metodos):
    ax.imshow(foto.resize((48, 48), metodo))
    ax.set_title(f"48 × 48, {nome}")
for ax in eixos:
    ax.axis("off")
fig.tight_layout()
fig.savefig("tamanho.png", dpi=300)
