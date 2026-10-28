import torch
from torch import nn

torch.manual_seed(0)
x = torch.randn(1, 16, 8, 8)              # 16 canais, 8 × 8
conv = nn.Conv2d(16, 4, kernel_size=1)    # 16 canais → 4
print("pesos:", tuple(conv.weight.shape))

W = conv.weight[:, :, 0, 0]               # matriz 4 × 16
pixel = x[0, :, 2, 5]                     # o vetor de um pixel
print("conv 1×1 no pixel (2, 5):",
      conv(x)[0, :, 2, 5].detach().numpy().round(4))
print("W · pixel + b:          ",
      (W @ pixel + conv.bias).detach().numpy().round(4))
