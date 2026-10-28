import torch
from torch import nn

from folha.conjunto import Folhas
from folha.redes import resnet_pequena

x, y = next(iter(torch.utils.data.DataLoader(Folhas("treino"),
                                             batch_size=64)))
for nome, residual in [("simples", False), ("residual", True)]:
    torch.manual_seed(0)
    rede = resnet_pequena(3, residual)
    nn.CrossEntropyLoss()(rede(x), y).backward()
    primeira = rede[0].weight.grad.norm().item()
    ultima = rede[-1].weight.grad.norm().item()
    print(f"{nome:9} gradiente na primeira {primeira:.2e},"
          f" na última {ultima:.2e}")
