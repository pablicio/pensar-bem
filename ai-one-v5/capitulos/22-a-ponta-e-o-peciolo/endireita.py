import matplotlib.pyplot as plt
import torch
from torch.utils.data import TensorDataset
from torchvision.transforms import v2

from folha.conjunto import CLASSES, DESVIO, MEDIA
from folha.emprestada import extrai, extratora, treina_cabeca
from folha.pontos import GiradasPontos, Mapas, angulo

media = torch.tensor(MEDIA).view(3, 1, 1)
desvio = torch.tensor(DESVIO).view(3, 1, 1)
rede = Mapas()
rede.load_state_dict(torch.load("pontos_mapas.pt"))
rede.eval()
giradas = GiradasPontos("girada")
with torch.no_grad():
    pontos = rede(giradas.x) * 128
graus = angulo(pontos)


def endireita(x, g, borda):
    """Gira a foto de volta; os cantos ficam pretos ou com a
    cor média da borda da foto."""
    cru = x * desvio + media
    cor = [0.0, 0.0, 0.0]
    if borda:
        anel = torch.cat([cru[:, 0], cru[:, -1],
                          cru[:, :, 0], cru[:, :, -1]], dim=1)
        cor = anel.mean(dim=1).tolist()
    volta = v2.functional.rotate(cru, g, fill=cor)
    return (volta - media) / desvio


pretas = torch.stack([endireita(x, g.item(), False)
                      for x, g in zip(giradas.x, graus)])
bordas = torch.stack([endireita(x, g.item(), True)
                      for x, g in zip(giradas.x, graus)])

# a cabeça do capítulo 16, treinada com folhas em pé
xt, yt = torch.load("caracteristicas.pt")["treino"]
cabeca = treina_cabeca(xt, yt)
resnet = extratora()
y = torch.tensor([CLASSES.index(v) for v in giradas.verdade])
CASOS = [("giradas", giradas.x),
         ("endireitadas, cantos pretos", pretas),
         ("endireitadas, cantos da cor da borda", bordas)]
for nome, fotos in CASOS:
    f, _ = extrai(resnet, TensorDataset(fotos, y))
    acerto = (cabeca(f).argmax(dim=1) == y).float().mean()
    print(f"{nome:37} {acerto:.1%}")

fig, eixos = plt.subplots(2, 4, figsize=(8, 4.2))
for j in range(4):
    cima, baixo = eixos[0, j], eixos[1, j]
    cima.imshow((giradas.x[j] * desvio + media).clamp(0, 1)
                .permute(1, 2, 0))
    ponta, peciolo = pontos[j]
    cima.plot(*ponta, "o", color="yellow", ms=5)
    cima.plot(*peciolo, "s", color="red", ms=5)
    cima.set_title(f"{graus[j]:.0f}°", fontsize=8)
    baixo.imshow((bordas[j] * desvio + media).clamp(0, 1)
                 .permute(1, 2, 0))
for ax in eixos.flat:
    ax.axis("off")
fig.tight_layout()
fig.savefig("endireitadas.png", dpi=300)
