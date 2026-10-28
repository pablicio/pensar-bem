import matplotlib.pyplot as plt
import torch
from torch import nn

from folha.conjunto import Folhas

# a primeira camada como foi sorteada (mesma semente do treino)
# e como ficou depois das dez épocas
torch.manual_seed(0)
antes = nn.Conv2d(3, 16, 5).weight.detach()
estado = torch.load("modelos/cnn.pt")
depois = estado["0.weight"]


def norma(t):
    return t.flatten(1).norm(dim=1)      # uma por filtro


mudanca = norma(depois - antes) / norma(antes)
print("quanto cada filtro mudou, em proporção:")
print(mudanca.numpy().round(2))

# o que cada filtro acende numa folha de ferrugem do campo
camada = nn.Conv2d(3, 16, 5, stride=2, padding=2)
camada.load_state_dict({"weight": depois,
                        "bias": estado["0.bias"]})
valid = Folhas("validacao")
i = next(i for i, f in enumerate(valid.linhas)
         if f["verdade"] == "ferrugem"
         and f["fundo"] != "mesa")
with torch.no_grad():
    mapas = torch.relu(camada(valid[i][0][None]))[0]
fig, eixos = plt.subplots(2, 9, figsize=(10, 2.5))
eixos[0, 0].imshow(valid.imagens[i].permute(1, 2, 0))
for k in range(16):
    ax = eixos[(k + 1) // 9, (k + 1) % 9]
    ax.imshow(mapas[k], cmap="gray")
for ax in eixos.flat:
    ax.axis("off")
fig.tight_layout()
fig.savefig("mapas.png", dpi=300)
