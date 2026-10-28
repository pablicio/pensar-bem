import matplotlib.pyplot as plt
import torch
from torch import nn

from folha.conjunto import Folhas
from folha.resnet import resnet_pequena
from folha.treino import acuracia, fixar_semente, lotes
from folha.treino import treinar_epoca

treino, valid = Folhas("treino"), Folhas("validacao")
fig, ax = plt.subplots(figsize=(6, 3.6))
for taxa in (1e-3, 1e-2):
    for normaliza in (False, True):
        fixar_semente(0, nucleos=4)
        rede = resnet_pequena(3, normaliza)
        otimizador = torch.optim.Adam(rede.parameters(),
                                      lr=taxa)
        carregador = lotes(treino, 64, semente=1)
        perdas = [treinar_epoca(rede, carregador, otimizador,
                                nn.CrossEntropyLoss())
                  for _ in range(10)]
        acerto = acuracia(rede, lotes(valid, 256))
        com = "com" if normaliza else "sem"
        nome = f"lr {taxa:g}, {com} BN"
        print(f"{nome:17} perda {perdas[-1]:.3f};"
              f" acerto {acerto:.1%}")
        ax.plot(range(1, 11), perdas, marker="o", label=nome)
torch.save(rede.state_dict(), "resnet_bn.pt")
ax.set_xlabel("época")
ax.set_ylabel("perda no treino")
ax.legend()
fig.tight_layout()
fig.savefig("normaliza.png", dpi=300)
