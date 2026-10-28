import torch
from torch import nn

from leitora.dados import MNIST
from leitora.modelo import MLP
from leitora.treino import (carregar, fixar_semente, lotes,
                            salvar, treinar_epoca)

treino = MNIST("treino")
perda_fn = nn.CrossEntropyLoss()


def novo():
    fixar_semente(0)
    modelo = MLP((100,), normaliza=True, dropout=0.2)
    otimizador = torch.optim.Adam(modelo.parameters())
    return modelo, otimizador, lotes(treino, 64, semente=1)


# quatro épocas seguidas
modelo, otimizador, carregador = novo()
for epoca in range(4):
    treinar_epoca(modelo, carregador, otimizador, perda_fn)
direto = modelo.state_dict()

# duas épocas, salva, "desliga", carrega, mais duas
modelo, otimizador, carregador = novo()
for epoca in range(2):
    treinar_epoca(modelo, carregador, otimizador, perda_fn)
salvar("leitora.pt", modelo, otimizador, carregador, epoca=2)
del modelo, otimizador, carregador

modelo, otimizador, carregador = novo()   # do zero, outra vez
inicio = carregar("leitora.pt", modelo, otimizador, carregador)
for epoca in range(inicio, 4):
    treinar_epoca(modelo, carregador, otimizador, perda_fn)
retomado = modelo.state_dict()

print(f"retomado da época {inicio}")
iguais = all(torch.equal(direto[k], retomado[k])
             for k in direto)
print("4 épocas seguidas e 2 + 2 dão os mesmos pesos:", iguais)
print("o checkpoint guarda:")
print("  " + ", ".join(torch.load("leitora.pt")))
