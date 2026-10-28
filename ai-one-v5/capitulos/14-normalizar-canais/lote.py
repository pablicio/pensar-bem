import copy

import torch

from folha.conjunto import CLASSES, Folhas
from folha.resnet import resnet_pequena
from folha.treino import lotes

valid = Folhas("validacao")
rede = resnet_pequena(3)
rede.load_state_dict(torch.load("resnet_bn.pt"))
salvo = copy.deepcopy(rede.state_dict())
x, y = valid[7]
vizinhas, _ = next(iter(lotes(valid, 64)))
lote = torch.cat([x[None], vizinhas[1:]])   # a foto e mais 63


@torch.no_grad()
def resposta(entrada):
    """A classe e a probabilidade dadas à primeira foto."""
    p = torch.softmax(rede(entrada), dim=1)[0]
    return f"{CLASSES[p.argmax()]} {p.max():.0%}"


print("foto 7, classe certa:", CLASSES[y])
for modo in ("train", "eval"):
    getattr(rede, modo)()
    print(f"{modo:6} sozinha: {resposta(x[None]):17}"
          f" no lote de 64: {resposta(lote)}")
    rede.load_state_dict(salvo)     # adiante se vê por quê


@torch.no_grad()
def acerto(tamanho):
    certas = 0
    for xs, ys in lotes(valid, tamanho):
        certas += (rede(xs).argmax(dim=1) == ys).sum().item()
    return certas / len(valid)


rede.eval()
print(f"avaliação, qualquer lote: {acerto(64):.1%}")
rede.train()
for tamanho in (1, 8, 64):
    certas = acerto(tamanho)
    print(f"treino, lotes de {tamanho:2}: {certas:.1%}")
