import matplotlib.pyplot as plt
import torch
from torch import nn

from folha.conjunto import Folhas
from folha.custo import parametros
from folha.redes import resnet_pequena
from folha.treino import acuracia, fixar_semente, lotes
from folha.treino import treinar_epoca

treino, valid = Folhas("treino"), Folhas("validacao")
REDES = [("simples, 8 camadas", 1, False),
         ("simples, 20 camadas", 3, False),
         ("residual, 20 camadas", 3, True)]
fig, ax = plt.subplots(figsize=(6, 3.6))
for nome, blocos, residual in REDES:
    fixar_semente(0, nucleos=4)
    rede = resnet_pequena(blocos, residual)
    otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
    carregador = lotes(treino, 64, semente=1)
    perdas = [treinar_epoca(rede, carregador, otimizador,
                            nn.CrossEntropyLoss())
              for _ in range(10)]
    acerto = acuracia(rede, lotes(valid, 256))
    print(f"{nome:21} {parametros(rede):8,} parâm.;"
          f" perda {perdas[-1]:.3f}; acerto {acerto:.1%}")
    ax.plot(range(1, 11), perdas, marker="o", label=nome)
ax.set_xlabel("época")
ax.set_ylabel("perda no treino")
ax.legend()
fig.tight_layout()
fig.savefig("curvas.png", dpi=300)
