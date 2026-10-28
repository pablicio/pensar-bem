import torch
from torch import nn

from folha.conjunto import Folhas
from folha.redes import rede_global

rede = rede_global()
campo, salto = 1, 1          # em pixels da foto
print(f"{'camada':12} {'campo':>6} {'salto':>6}")
for camada in rede:
    if isinstance(camada, (nn.Conv2d, nn.MaxPool2d)):
        k = camada.kernel_size
        k = k[0] if isinstance(k, tuple) else k
        s = camada.stride
        s = s[0] if isinstance(s, tuple) else s
        campo += (k - 1) * salto
        salto *= s
        nome = type(camada).__name__
        print(f"{nome:12} {campo:6} {salto:6}")


def alcance(modelo, x):
    """Quantas linhas da foto mexem no pixel (4, 4) do fim."""
    x = x.clone().requires_grad_(True)
    mapa = modelo[:-3](x)              # antes da média global
    mapa[0, :, 4, 4].sum().backward()
    linhas = (x.grad.abs().sum(dim=(0, 1, 3)) > 0).nonzero()
    return linhas.max().item() - linhas.min().item() + 1


foto = Folhas("validacao")[0][0][None]
print("linhas da foto que mexem no pixel (4, 4) do fim:",
      alcance(rede, foto))
