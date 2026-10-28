import matplotlib.pyplot as plt
import torch
from matplotlib.colors import ListedColormap

from folha.conjunto import DESVIO, MEDIA
from folha.unet import Mascaras, UNet

valid = Mascaras("validacao")
redes = {}
VERSOES = [("sem atalhos", "sem_atalhos.pt", False),
           ("U-Net", "unet.pt", True)]
for nome, arquivo, atalhos in VERSOES:
    redes[nome] = UNet(atalhos=atalhos)
    redes[nome].load_state_dict(torch.load(arquivo))
    redes[nome].eval()
CORES = ListedColormap(["black", "green", "orange"])
media = torch.tensor(MEDIA).view(3, 1, 1)
desvio = torch.tensor(DESVIO).view(3, 1, 1)
# três fotos com bastante lesão
area = (valid.mascaras == 2).flatten(1).sum(dim=1)
ordem = area.argsort(descending=True)
escolhidas = ordem[[5, 40, 80]].tolist()
fig, eixos = plt.subplots(3, 4, figsize=(7, 5.4))
for linha, i in zip(eixos, escolhidas):
    x, m = valid[i]
    linha[0].imshow((x * desvio + media).clamp(0, 1)
                    .permute(1, 2, 0))
    linha[1].imshow(m, cmap=CORES, vmin=0, vmax=2)
    for ax, (nome, rede) in zip(linha[2:], redes.items()):
        with torch.no_grad():
            p = rede(x[None]).argmax(dim=1)[0]
        ax.imshow(p, cmap=CORES, vmin=0, vmax=2)
for ax, titulo in zip(eixos[0], ["foto", "máscara certa",
                                 "sem atalhos", "U-Net"]):
    ax.set_title(titulo, fontsize=8)
for ax in eixos.flat:
    ax.axis("off")
fig.tight_layout()
fig.savefig("mascaras.png", dpi=300)
