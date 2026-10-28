import torch
from torch import nn

torch.manual_seed(0)
escala = torch.tensor([1.0, 4.0, 0.5]).view(1, 3, 1, 1)
centro = torch.tensor([2.0, -3.0, 10.0]).view(1, 3, 1, 1)
x = torch.randn(8, 3, 5, 5) * escala + centro  # 8 fotos

linhas = x.transpose(0, 1).reshape(3, -1)  # canal por linha
print("matriz dos canais:", tuple(linhas.shape))
media = linhas.mean(dim=1)
var = linhas.var(dim=1, unbiased=False)
print("média:    ", media.numpy().round(3))
print("variância:", var.numpy().round(3))

xn = (x - media.view(1, 3, 1, 1)) / torch.sqrt(
    var.view(1, 3, 1, 1) + 1e-5)
bn = nn.BatchNorm2d(3)
diferenca = (bn(x) - xn).abs().max()
print(f"diferença para o BatchNorm2d: {diferenca:.1e}")
print("média móvel:   ", bn.running_mean.numpy().round(3))
print("variância móvel:", bn.running_var.numpy().round(3))
