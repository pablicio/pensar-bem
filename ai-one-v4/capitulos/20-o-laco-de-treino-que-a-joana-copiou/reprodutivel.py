import torch
from torch import nn

from leitora.dados import MNIST
from leitora.modelo import MLP
from leitora.treino import (avaliar, fixar_semente, lotes,
                            treinar_epoca)

treino, teste = MNIST("treino"), MNIST("teste")
pesos = []
for execucao in (1, 2):
    fixar_semente(0)
    modelo = MLP((100,), normaliza=True, dropout=0.2)
    otimizador = torch.optim.Adam(modelo.parameters())
    perda_fn = nn.CrossEntropyLoss()
    carregador = lotes(treino, 64, semente=1)
    for epoca in range(2):
        treinar_epoca(modelo, carregador, otimizador, perda_fn)
    _, acerto = avaliar(modelo, lotes(teste, 1000), perda_fn)
    print(f"execução {execucao}: teste {acerto:.2%}")
    pesos.append(modelo.state_dict())

iguais = all(torch.equal(pesos[0][k], pesos[1][k])
             for k in pesos[0])
print("os pesos das duas execuções são idênticos:", iguais)
