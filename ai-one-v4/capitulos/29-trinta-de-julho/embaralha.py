import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.utils.data import TensorDataset

from leitora.carrega import ARQUITETURA
from leitora.dados import MNIST
from leitora.modelo import MLP
from leitora.treino import (avaliar, fixar_semente, lotes,
                            treinar_epoca)

treino, teste = MNIST("treino"), MNIST("teste")
# uma só ordem embaralhada, a mesma para todas as imagens
sorteador = torch.Generator().manual_seed(30)
ordem = torch.randperm(784, generator=sorteador)


def embaralha(d):
    x = d.imagens.reshape(-1, 784)[:, ordem]
    return TensorDataset(x.reshape(-1, 28, 28), d.rotulos)


for nome, tr, te in [("pixels no lugar", treino, teste),
                     ("pixels embaralhados", embaralha(treino),
                      embaralha(teste))]:
    fixar_semente(0)
    modelo = MLP(**ARQUITETURA)
    otimizador = torch.optim.Adam(modelo.parameters())
    agenda = torch.optim.lr_scheduler.CosineAnnealingLR(
        otimizador, T_max=8)
    perda_fn = nn.CrossEntropyLoss()
    carregador = lotes(tr, 64, semente=1)
    for epoca in range(8):
        treinar_epoca(modelo, carregador, otimizador, perda_fn)
        agenda.step()
    _, acerto = avaliar(modelo, lotes(te, 1000), perda_fn)
    print(f"{nome:20} {acerto:.2%}")

fig, eixos = plt.subplots(2, 6, figsize=(9, 3.4))
misturado = embaralha(teste)
for j in range(6):
    eixos[0, j].imshow(teste.imagens[j], cmap="gray_r")
    eixos[1, j].imshow(misturado[j][0], cmap="gray_r")
    for ax in eixos[:, j]:
        ax.axis("off")
fig.tight_layout()
fig.savefig("embaralhados.png", dpi=300)
