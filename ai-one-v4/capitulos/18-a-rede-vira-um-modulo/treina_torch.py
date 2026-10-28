import torch
from torch import nn

from leitora.modelo import MLP, conta_parametros
from numpy_mlp.dados import mnist_vetores

torch.manual_seed(0)
(X, y), (Xv, yv), _ = mnist_vetores()
X, y = torch.tensor(X), torch.tensor(y).long()   # copia
Xv, yv = torch.tensor(Xv), torch.tensor(yv).long()

modelo = MLP()
print(modelo)
print(f"parâmetros: {conta_parametros(modelo):,}")
perda_fn = nn.CrossEntropyLoss()          # softmax + entropia
otimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)

for epoca in range(1, 11):
    ordem = torch.randperm(len(X))
    for k in range(0, len(X), 64):
        i = ordem[k:k + 64]
        perda = perda_fn(modelo(X[i]), y[i])
        otimizador.zero_grad()            # zera
        perda.backward()                  # deriva
        otimizador.step()                 # um passo
    with torch.no_grad():
        previsto = modelo(Xv).argmax(dim=1)
        acerto = (previsto == yv).float().mean()
    if epoca % 2 == 0:
        print(f"época {epoca:2}: validação {acerto:.2%}")
