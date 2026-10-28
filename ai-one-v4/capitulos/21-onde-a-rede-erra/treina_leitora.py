from pathlib import Path

import torch
from torch import nn

from leitora.carrega import ARQUITETURA
from leitora.dados import MNIST
from leitora.modelo import MLP
from leitora.treino import (avaliar, fixar_semente, lotes,
                            treinar_epoca)

fixar_semente(0)
treino, teste = MNIST("treino"), MNIST("teste")
modelo = MLP(**ARQUITETURA)
otimizador = torch.optim.Adam(modelo.parameters())
agenda = torch.optim.lr_scheduler.CosineAnnealingLR(otimizador,
                                                    T_max=8)
perda_fn = nn.CrossEntropyLoss()
carregador = lotes(treino, 64, semente=1)
for epoca in range(1, 9):
    treinar_epoca(modelo, carregador, otimizador, perda_fn)
    agenda.step()               # o cosseno, uma vez por época
_, acerto = avaliar(modelo, lotes(teste, 1000), perda_fn)
print(f"MNIST, teste: {acerto:.2%}")
Path("modelos").mkdir(exist_ok=True)
torch.save(modelo.state_dict(), "modelos/leitora_mnist.pt")
