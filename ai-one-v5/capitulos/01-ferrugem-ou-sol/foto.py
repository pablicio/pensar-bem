import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image

foto = np.array(Image.open("dados/brutos/fotos/000068.jpg"))
print("formato:", foto.shape, "· tipo:", foto.dtype)
print("menor e maior valor:", foto.min(), foto.max())
for nome, (y, x) in {"pústula": (61, 103), "folha": (150, 128),
                     "terra": (20, 20)}.items():
    print(f"{nome:8} linha {y:3}, coluna {x:3}: {foto[y, x]}")

# no PyTorch, os canais vêm primeiro e os valores de 0 a 1
tensor = torch.from_numpy(foto).permute(2, 0, 1).float() / 255
print("tensor:", tuple(tensor.shape), tensor.dtype)
print("o mesmo pixel:", tensor[:, 61, 103])

fig, eixos = plt.subplots(1, 4, figsize=(9, 2.6))
eixos[0].imshow(foto)
eixos[0].set_title("a foto")
for c, nome in enumerate(["vermelho", "verde", "azul"], 1):
    eixos[c].imshow(foto[:, :, c - 1], cmap="gray", vmin=0,
                    vmax=255)
    eixos[c].set_title(nome)
for ax in eixos:
    ax.axis("off")
fig.tight_layout()
fig.savefig("canais.png", dpi=300)
