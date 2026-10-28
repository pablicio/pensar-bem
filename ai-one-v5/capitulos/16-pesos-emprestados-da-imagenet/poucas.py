import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.utils.data import Subset

from folha.conjunto import Folhas
from folha.emprestada import treina_cabeca
from folha.redes import rede_global
from folha.treino import acuracia, fixar_semente, lotes
from folha.treino import treinar_epoca

treino, valid = Folhas("treino"), Folhas("validacao")
matrizes = torch.load("caracteristicas.pt")
xt, yt = matrizes["treino"]
xv, yv = matrizes["validacao"]
sorteador = torch.Generator().manual_seed(0)
sorteio = torch.randperm(len(treino), generator=sorteador)
FRACOES = (0.05, 0.1, 0.25, 1.0)
zero, emprestada = [], []
print("fotos  épocas  do zero  emprestada")
for fracao in FRACOES:
    escolhidas = sorteio[:int(fracao * len(treino))]
    cabeca = treina_cabeca(xt[escolhidas], yt[escolhidas])
    emprestada.append((cabeca(xv).argmax(dim=1) == yv)
                      .float().mean().item())
    epocas = int(30 / fracao ** 0.5)  # menos fotos, + épocas
    fixar_semente(0, nucleos=4)
    rede = rede_global()
    otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
    parte = Subset(treino, escolhidas.tolist())
    carregador = lotes(parte, 64, semente=1)
    for _ in range(epocas):
        treinar_epoca(rede, carregador, otimizador,
                      nn.CrossEntropyLoss())
    zero.append(acuracia(rede, lotes(valid, 256)))
    print(f"{len(escolhidas):5} {epocas:7} {zero[-1]:8.1%}"
          f" {emprestada[-1]:11.1%}")

fotos = [int(f * len(treino)) for f in FRACOES]
fig, ax = plt.subplots(figsize=(6, 3.4))
ax.plot(fotos, zero, marker="o", label="do zero")
ax.plot(fotos, emprestada, marker="s",
        label="ResNet-18 congelada")
ax.set_xscale("log")
ax.set_xlabel("fotos de treino")
ax.set_ylabel("acerto na validação")
ax.legend()
fig.tight_layout()
fig.savefig("poucas.png", dpi=300)
