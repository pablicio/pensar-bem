import matplotlib.pyplot as plt
import torch
from torchvision.transforms import v2

from folha.conjunto import Folhas

torch.manual_seed(3)
fotos = Folhas("treino")
cru = fotos.imagens.float() / 255           # sem normalizar


def primeira(classe):
    """A primeira foto da classe tirada sobre a terra."""
    i = next(i for i, f in enumerate(fotos.linhas)
             if f["verdade"] == classe
             and f["fundo"] == "terra")
    return cru[i]


sadia, sol = primeira("sadia"), primeira("sol")
GIRA = v2.Compose([v2.RandomHorizontalFlip(),
                   v2.RandomRotation(180)])
MATIZES = [0, 0.04, 0.08, 0.15, -0.12]

fig, eixos = plt.subplots(2, 6, figsize=(9, 3.4))
for ax in eixos[0]:
    ax.imshow(GIRA(sadia).permute(1, 2, 0))
for ax, h in zip(eixos[1], MATIZES):
    matizada = v2.functional.adjust_hue(sadia, h)
    ax.imshow(matizada.permute(1, 2, 0))
    ax.set_title(f"matiz {h:+.2f}", fontsize=8)
eixos[1, 5].imshow(sol.permute(1, 2, 0))
eixos[1, 5].set_title("sol, de verdade", fontsize=8)
for ax in eixos.flat:
    ax.axis("off")
fig.tight_layout()
fig.savefig("aumentos.png", dpi=300)
