import torch

from leitora.carrega import leitora, probabilidades
from leitora.dados import MNIST, CaixasDoCartao

modelo = leitora()
conjuntos = {"MNIST, teste": MNIST("teste"),
             "cartões, validação": CaixasDoCartao("validacao")}
for nome, dados in conjuntos.items():
    y = dados.rotulos
    p = probabilidades(modelo, dados.imagens)
    previsto = p.argmax(dim=1)
    print(f"{nome}: {(previsto == y).float().mean():.2%}"
          f" de {len(y):,}")

# a matriz de confusão dos cartões: linha = era, coluna = leu
matriz = torch.zeros(10, 10, dtype=torch.long)
for era, leu in zip(y, previsto):
    matriz[era, leu] += 1
print()
print("era/leu" + "".join(f"{d:5}" for d in range(10)))
for d in range(10):
    linha = "".join(f"{v:5}" for v in matriz[d].tolist())
    acerto = matriz[d, d] / matriz[d].sum()
    print(f"{d:7}{linha}   {acerto:6.1%}")
