"""Peças do PyTorch contra a mesma conta em NumPy."""
import numpy as np
import torch
from torch import nn

torch.manual_seed(0)
x = torch.randn(5, 4)
y = torch.tensor([0, 2, 1, 1, 0])
X = x.numpy()


def mostra(nome, torch_, numpy_):
    igual = np.allclose(torch_, numpy_, atol=1e-6)
    print(f"{nome:28} {'igual' if igual else 'DIFERENTE'}")


camada = nn.Linear(4, 3)
W = camada.weight.detach().numpy()        # formato (3, 4)
b = camada.bias.detach().numpy()
z = camada(x)
mostra("nn.Linear", z.detach(), X @ W.T + b)

Z = z.detach().numpy()
p = np.exp(Z - Z.max(1, keepdims=True))
p /= p.sum(1, keepdims=True)
mostra("softmax", z.softmax(dim=1).detach(), p)

perda = nn.CrossEntropyLoss()(z, y)
mostra("nn.CrossEntropyLoss", perda.detach(),
       -np.log(p[np.arange(5), y.numpy()]).mean())

perda.backward()
G = (p - np.eye(3)[y.numpy()]) / 5        # dL/dz, o cap. 8
mostra("backward, em W", camada.weight.grad, G.T @ X)
mostra("backward, em b", camada.bias.grad, G.sum(0))

norm = nn.BatchNorm1d(4)
media, var = X.mean(0), X.var(0)
mostra("nn.BatchNorm1d (treino)", norm(x).detach(),
       (X - media) / np.sqrt(var + 1e-5))

otimizador = torch.optim.Adam(camada.parameters(), lr=0.01)
antes = camada.weight.detach().numpy().copy()
g = camada.weight.grad.numpy()
otimizador.step()
m, s = 0.1 * g, 0.001 * g ** 2     # o primeiro passo
passo = 0.01 * (m / 0.1) / (np.sqrt(s / 0.001) + 1e-8)
mostra("Adam, um passo", camada.weight.detach(), antes - passo)
