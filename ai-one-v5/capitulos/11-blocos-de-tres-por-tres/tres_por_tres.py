import torch
from torch import nn

from folha.custo import multiplicacoes, parametros

C = 64
uma = nn.Conv2d(C, C, 5, padding=2)
duas = nn.Sequential(nn.Conv2d(C, C, 3, padding=1), nn.ReLU(),
                     nn.Conv2d(C, C, 3, padding=1))
x = torch.zeros(1, C, 32, 32)
for nome, camada in [("uma 5×5", uma), ("duas 3×3", duas)]:
    print(f"{nome:9} parâmetros {parametros(camada):7,}"
          f"  multiplicações {multiplicacoes(camada, x):11,}")


def alcance(camada):
    """Quantas colunas da entrada mexem no pixel do centro."""
    x = torch.randn(1, C, 32, 32, requires_grad=True)
    camada(x)[0, :, 16, 16].sum().backward()
    colunas = (x.grad.abs().sum(dim=(0, 1, 2)) > 0).nonzero()
    return colunas.max().item() - colunas.min().item() + 1


torch.manual_seed(0)
print("campo receptivo: uma 5×5 →", alcance(uma),
      "· duas 3×3 →", alcance(duas))
