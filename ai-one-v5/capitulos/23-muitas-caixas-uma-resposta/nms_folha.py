import matplotlib.pyplot as plt
import torch
from matplotlib.patches import Rectangle
from torchvision.ops import nms as nms_torchvision

from folha.conjunto import DESVIO, MEDIA
from folha.deteccao import Janelas, decodifica, nms
from folha.deteccao import rede_janelas

valid = Janelas("validacao")
rede = rede_janelas()
rede.load_state_dict(torch.load("janelas.pt"))
rede.eval()

# a foto de uma lesão só com mais caixas antes da supressão
melhor, mais = None, -1
with torch.no_grad():
    for i in range(len(valid)):
        if len(valid.caixas[i]) == 1:
            saida = rede(valid[i][0][None])[0]
            caixas, notas = decodifica(saida)
            if len(caixas) > mais:
                melhor, mais = i, len(caixas)
x = valid[melhor][0]
with torch.no_grad():
    caixas, notas = decodifica(rede(x[None])[0])
print(f"foto {valid.fotos.linhas[melhor]['foto']}: 1 lesão,"
      f" {len(caixas)} caixas acima de 0,5")
ordenadas = notas.sort(descending=True).values
print("notas:", ordenadas.numpy().round(2))
mao = nms(caixas, notas, 0.3)
pronta = nms_torchvision(caixas, notas, 0.3)
print("guardadas à mão:", mao.tolist(),
      " pela torchvision:", pronta.tolist())

imagem = (x * torch.tensor(DESVIO).view(3, 1, 1)
          + torch.tensor(MEDIA).view(3, 1, 1)).clamp(0, 1)
fig, eixos = plt.subplots(1, 2, figsize=(6, 3.2))
QUADROS = [(eixos[0], "antes", range(len(caixas))),
           (eixos[1], "depois", mao.tolist())]
for ax, titulo, quais in QUADROS:
    ax.imshow(imagem.permute(1, 2, 0))
    for k in quais:
        c = caixas[k]
        ax.add_patch(Rectangle(c[:2], *(c[2:] - c[:2]),
                               fill=False, ec="yellow",
                               lw=0.8))
    certa = valid.caixas[melhor][0]
    ax.add_patch(Rectangle(certa[:2], *(certa[2:] - certa[:2]),
                           fill=False, ec="white", lw=1.2,
                           ls="--"))
    ax.set_title(titulo, fontsize=9)
    ax.axis("off")
fig.tight_layout()
fig.savefig("nms.png", dpi=300)
