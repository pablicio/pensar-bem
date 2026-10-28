import matplotlib.pyplot as plt
import torch

from folha.conjunto import CLASSES

x, y = torch.load("caracteristicas.pt")["validacao"]
centrada = x - x.mean(dim=0)              # 449 × 512
U, S, Vt = torch.linalg.svd(centrada, full_matrices=False)
plano = centrada @ Vt[:2].T               # 449 × 2
parte = S[:2] ** 2 / (S ** 2).sum()
print("variância nas duas direções:", parte.numpy().round(3))

fig, ax = plt.subplots(figsize=(6, 4.2))
for i, classe in enumerate(CLASSES):
    pontos = plano[y == i]
    ax.scatter(pontos[:, 0], pontos[:, 1], s=9, label=classe)
ax.set_xlabel("primeira componente")
ax.set_ylabel("segunda componente")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("mapa.png", dpi=300)
