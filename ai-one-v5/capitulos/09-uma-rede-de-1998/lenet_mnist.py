import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import TensorDataset

from folha.redes import lenet
from folha.treino import acuracia, fixar_semente, lotes
from folha.treino import treinar_epoca
from mnist import carregar


def tensores(parte):
    """Os dígitos com moldura de 2: os 32 × 32 de 1998."""
    imagens, rotulos = carregar(parte)
    x = torch.tensor(imagens / 255, dtype=torch.float32)
    x = x[:, None]                      # um canal só
    return TensorDataset(F.pad(x, (2, 2, 2, 2)),
                         torch.tensor(rotulos).long())


fixar_semente(0)
treino, teste = tensores("treino"), tensores("teste")
rede = lenet()
for nome, p in rede.named_parameters():
    if nome.endswith("weight"):
        formato = str(tuple(p.shape))
        print(f"{nome:9} {formato:16} {p.numel():>7,}")
total = sum(p.numel() for p in rede.parameters())
print(f"total, com os vieses: {total:,}")
otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
carregador = lotes(treino, 64, semente=1)
for epoca in range(1, 4):
    treinar_epoca(rede, carregador, otimizador,
                  nn.CrossEntropyLoss())
    acerto = acuracia(rede, lotes(teste, 1000))
    print(f"época {epoca}: teste {acerto:.2%}")
