import matplotlib.pyplot as plt
import torch

from folha.conjunto import CLASSES, DESVIO, MEDIA, Folhas
from folha.siamesa import Projecao, distancias

m = torch.load("caracteristicas.pt")
(xt, yt), (xv, yv) = m["treino"], m["validacao"]
projecao = Projecao()
projecao.load_state_dict(torch.load("projecao.pt"))
projecao.eval()
with torch.no_grad():
    zt, zv = projecao(xt), projecao(xv)
treino, valid = Folhas("treino"), Folhas("validacao")
media = torch.tensor(MEDIA).view(3, 1, 1)
desvio = torch.tensor(DESVIO).view(3, 1, 1)


def mostra(ax, x, titulo):
    imagem = (x * desvio + media).clamp(0, 1)
    ax.imshow(imagem.permute(1, 2, 0))
    ax.set_title(titulo, fontsize=7)
    ax.axis("off")


consultas = [int((yv == CLASSES.index(c)).nonzero()[0])
             for c in ("phoma", "bicho-mineiro")]
fig, eixos = plt.subplots(2, 6, figsize=(8, 3))
for linha, i in zip(eixos, consultas):
    titulo = f"consulta: {CLASSES[yv[i]]}"
    mostra(linha[0], valid[i][0], titulo)
    d = distancias(zv[i][None], zt)[0]
    for ax, j in zip(linha[1:], d.argsort()[:5].tolist()):
        legenda = f"{CLASSES[yt[j]]} {d[j]:.3f}"
        mostra(ax, treino[j][0], legenda)
fig.tight_layout()
fig.savefig("vizinhas.png", dpi=300)
