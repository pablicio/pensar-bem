import time

import numpy as np
import torch
from torch import nn

from rio.numpy_treino import tarefa_soma

torch.manual_seed(0)
sorteio = np.random.default_rng(0)
x, y = tarefa_soma(sorteio, 2000, 50)
xv, yv = tarefa_soma(sorteio, 500, 50)
x, y = torch.tensor(x, dtype=torch.float32), torch.tensor(y)
xv = torch.tensor(xv, dtype=torch.float32)
yv = torch.tensor(yv)


class Soma(nn.Module):
    def __init__(self, celula):
        super().__init__()
        self.celula = celula(input_size=2, hidden_size=16,
                             batch_first=True)
        self.saida = nn.Linear(16, 1)

    def forward(self, x):
        estados, _ = self.celula(x)
        return self.saida(estados[:, -1]).squeeze(1)


EPOCAS = 30
Soma(nn.LSTM)(x[:16]).sum().backward()  # aquece a biblioteca
print("rede  parâmetros  s/época  erro na validação")
for celula in (nn.RNN, nn.LSTM, nn.GRU):
    modelo = Soma(celula)
    n = sum(p.numel() for p in modelo.parameters())
    pesos = modelo.parameters()
    otimizador = torch.optim.Adam(pesos, lr=0.003)
    inicio = time.perf_counter()
    for epoca in range(EPOCAS):
        for i in torch.randperm(len(x)).split(16):
            perda = nn.functional.mse_loss(modelo(x[i]),
                                           y[i].float())
            otimizador.zero_grad()
            perda.backward()
            nn.utils.clip_grad_norm_(modelo.parameters(), 1.0)
            otimizador.step()
    segundos = (time.perf_counter() - inicio) / EPOCAS
    with torch.no_grad():
        erro = nn.functional.mse_loss(modelo(xv), yv.float())
    print(f"{celula.__name__:5} {n:10d} {segundos:8.2f}"
          f" {erro:12.4f}")
