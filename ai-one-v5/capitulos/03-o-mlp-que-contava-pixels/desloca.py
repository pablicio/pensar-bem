import matplotlib.pyplot as plt
import torch
from torch import nn

from folha.conjunto import Folhas
from folha.treino import acuracia, lotes

mlp = nn.Sequential(nn.Flatten(),
                    nn.Linear(3 * 128 * 128, 256), nn.ReLU(),
                    nn.Linear(256, 6))
mlp.load_state_dict(torch.load("modelos/mlp.pt"))
valid = Folhas("validacao")
originais = valid.imagens.clone()

print("deslocamento  acerto")
fig, eixos = plt.subplots(1, 4, figsize=(9, 2.5))
for k, d in enumerate([0, 2, 4, 8, 16, 32]):
    # empurra as fotos d pixels para a direita
    valid.imagens = torch.roll(originais, d, dims=3)
    acerto = acuracia(mlp, lotes(valid, 256))
    print(f"{d:6} pixels  {acerto:6.1%}")
    if d in (0, 8, 16, 32):
        ax = eixos[[0, 8, 16, 32].index(d)]
        ax.imshow(valid.imagens[4].permute(1, 2, 0))
        ax.set_title(f"{d} pixels")
        ax.axis("off")
fig.tight_layout()
fig.savefig("desloca.png", dpi=300)

# o primeiro neurônio olha cada pixel com um peso próprio
pesos = mlp[1].weight[0].detach().reshape(3, 128, 128)
mapa = pesos.abs().sum(dim=0)
fig, ax = plt.subplots(figsize=(3, 3))
ax.imshow(mapa, cmap="magma")
ax.axis("off")
fig.tight_layout()
fig.savefig("pesos_mlp.png", dpi=500)
