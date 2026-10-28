import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image
from torch.nn import functional as F

from folha.conjunto import PASTA

# quantas vezes cada pixel da saída é somado: núcleo de uns
for k in (3, 4):
    uns = torch.ones(1, 1, 4, 4)
    conta = F.conv_transpose2d(uns, torch.ones(1, 1, k, k),
                               stride=2)
    lado = tuple(conta.shape[-2:])
    print(f"núcleo {k} × {k}, passo 2: saída {lado}")
    print(conta[0, 0, :7, :7].int().numpy())

# a máscara de uma folha, reduzida a 16 × 16 e ampliada a 64
m = Image.open(PASTA / "mascaras" / "000001.png")
m = np.array(m.resize((16, 16), Image.BOX)) > 0
x = torch.tensor(m.astype(np.float32))[None, None]
transp = F.conv_transpose2d(x, torch.ones(1, 1, 3, 3) / 2.25,
                            stride=2, padding=1,
                            output_padding=1)
transp = F.interpolate(transp, size=64, mode="nearest")
bilinear = F.interpolate(x, size=64, mode="bilinear")
QUADROS = [(x, "máscara 16 × 16"),
           (transp, "transposta 3 × 3, passo 2"),
           (bilinear, "interpolação bilinear")]
fig, eixos = plt.subplots(1, 3, figsize=(7, 2.5))
for ax, (img, titulo) in zip(eixos, QUADROS):
    ax.imshow(img[0, 0], cmap="gray", vmin=0, vmax=1.5,
              interpolation="nearest")
    ax.set_title(titulo, fontsize=8)
    ax.axis("off")
fig.tight_layout()
fig.savefig("tabuleiro.png", dpi=300)
