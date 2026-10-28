import torch
from torch import nn

from folha.conjunto import Folhas
from folha.resnet import resnet_pequena
from folha.treino import lotes

rede = resnet_pequena(3)
rede.load_state_dict(torch.load("resnet_bn.pt"))
rede.eval()
conv, bn = rede[0][0], rede[0][1]

escala = bn.weight / torch.sqrt(bn.running_var + bn.eps)
fundida = nn.Conv2d(3, 16, 3, 2, 1)
with torch.no_grad():
    peso = conv.weight * escala.view(16, 1, 1, 1)
    fundida.weight.copy_(peso)
    fundida.bias.copy_(bn.bias - bn.running_mean * escala)

x, _ = next(iter(lotes(Folhas("validacao"), 64)))
with torch.no_grad():
    diferenca = (rede[0](x) - fundida(x)).abs().max().item()
print(f"conv + BN contra a conv fundida: {diferenca:.1e}")
