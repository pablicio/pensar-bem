import matplotlib.pyplot as plt
import torch
from matplotlib.patches import Rectangle

from folha.conjunto import DESVIO, MEDIA
from folha.yolo import TIPOS, Grade, MiniYolo, detecta

ancoras = torch.load("ancoras.pt")
valid = Grade("validacao", ancoras)
rede = MiniYolo(ancoras)
rede.load_state_dict(torch.load("yolo.pt"))
rede.eval()
CORES = ["orange", "magenta", "cyan", "red", "yellow"]
media = torch.tensor(MEDIA).view(3, 1, 1)
desvio = torch.tensor(DESVIO).view(3, 1, 1)
# a primeira foto de cada um de quatro tipos
escolhidas = []
for t in (0, 1, 3, 4):
    for i, c in enumerate(valid.caixas):
        if len(c) and (c[:, 4] == t).all():
            escolhidas.append(i)
            break


def conta(n, um, varios):
    return f"{n} {um if n == 1 else varios}"


fig, eixos = plt.subplots(1, 4, figsize=(8, 2.4))
for ax, i in zip(eixos, escolhidas):
    x = valid[i][0]
    imagem = (x * desvio + media).clamp(0, 1)
    ax.imshow(imagem.permute(1, 2, 0))
    caixas, notas, tipos = detecta(rede, x)
    for c, n, t in zip(caixas, notas, tipos):
        if n > 0.3:
            ax.add_patch(Rectangle(c[:2], *(c[2:] - c[:2]),
                                   fill=False, lw=0.9,
                                   ec=CORES[t]))
    certo = TIPOS[int(valid.caixas[i][0, 4])]
    n = (notas > 0.3).sum().item()
    lesoes = len(valid.caixas[i])
    titulo = (f"{certo}: {conta(lesoes, 'lesão', 'lesões')}, "
              + conta(n, "caixa", "caixas"))
    ax.set_title(titulo, fontsize=7)
    ax.axis("off")
fig.tight_layout()
fig.savefig("yolo.png", dpi=300)
