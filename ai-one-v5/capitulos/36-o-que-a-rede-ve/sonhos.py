import matplotlib.pyplot as plt
import torch

from folha.conjunto import CLASSES, DESVIO, MEDIA
from folha.emprestada import extratora, treina_cabeca
from folha.treino import fixar_semente

fixar_semente(0, nucleos=4)
xt, yt = torch.load("caracteristicas.pt")["treino"]
cabeca = treina_cabeca(xt, yt)
rede = torch.nn.Sequential(extratora(), cabeca)
for p in rede.parameters():
    p.requires_grad_(False)
media = torch.tensor(MEDIA).view(3, 1, 1)
desvio = torch.tensor(DESVIO).view(3, 1, 1)
fig, eixos = plt.subplots(1, 6, figsize=(9, 1.9))
for ax, c in zip(eixos, range(6)):
    x = 0.1 * torch.randn(1, 3, 128, 128)
    x.requires_grad_(True)
    otimizador = torch.optim.Adam([x], lr=0.05)
    for passo in range(200):
        dx, dy = torch.randint(-4, 5, (2,)).tolist()
        tremida = torch.roll(x, (dx, dy), dims=(2, 3))
        nota = rede(tremida)[0, c]
        otimizador.zero_grad()
        (-nota + 0.01 * x.pow(2).mean()).backward()
        otimizador.step()
    img = (x.detach()[0] * desvio + media).clamp(0, 1)
    ax.imshow(img.permute(1, 2, 0))
    ax.set_title(CLASSES[c], fontsize=8)
    ax.axis("off")
    print(f"{CLASSES[c]:14} nota final {nota.item():6.1f}")
fig.tight_layout()
fig.savefig("sonhos.png", dpi=300)
