import torch
from torch import nn
from torch.utils.data import DataLoader

from leitora.dados import MNIST
from leitora.modelo import MLP

# o laço do tutorial, como a Joana copiou
for execucao in (1, 2):
    modelo = MLP((100,), normaliza=True, dropout=0.2)
    otimizador = torch.optim.Adam(modelo.parameters())
    perda_fn = nn.CrossEntropyLoss()
    treino = DataLoader(MNIST("treino"), batch_size=64,
                        shuffle=True)
    for epoca in range(2):
        for x, y in treino:
            perda = perda_fn(modelo(x), y)
            otimizador.zero_grad()
            perda.backward()
            otimizador.step()
    Xt, yt = MNIST("teste")[:]
    acerto = (modelo(Xt).argmax(dim=1) == yt).float().mean()
    print(f"execução {execucao}: teste {acerto:.2%}")
