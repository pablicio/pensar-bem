import torch
from torch import nn

from folha.convolucao import tamanho_saida

camadas = [nn.Conv2d(3, 16, 5),
           nn.Conv2d(16, 32, 5, stride=2),
           nn.Conv2d(32, 32, 3, stride=2, padding=1)]

print(f"{'camada':30} {'à mão':>12} {'PyTorch':>15}")
x = torch.zeros(1, 3, 128, 128)
n = 128
for c in camadas:
    k, s, p = c.kernel_size[0], c.stride[0], c.padding[0]
    n = tamanho_saida(n, k, s, p)
    x = c(x)
    nome = f"conv {k}×{k}, passo {s}, preench. {p}"
    mao = f"{c.out_channels}×{n}×{n}"
    print(f"{nome:30} {mao:>12} {str(tuple(x.shape[1:])):>15}")
print("achatado:", x.flatten(1).shape[1], "números")
