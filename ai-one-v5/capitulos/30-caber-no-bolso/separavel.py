import torch
from torch import nn

from folha.custo import multiplicacoes, parametros

C, S, H = 64, 128, 32                    # canais, saída, lado
comum = nn.Conv2d(C, S, 3, padding=1, bias=False)
separavel = nn.Sequential(
    nn.Conv2d(C, C, 3, padding=1, groups=C, bias=False),  # dw
    nn.Conv2d(C, S, 1, bias=False))                       # pw
x = torch.randn(1, C, H, H)
for nome, camada in (("comum 3×3", comum),
                     ("separável", separavel)):
    p = parametros(camada)
    m = multiplicacoes(camada, x)
    print(f"{nome:10} {p:7,} parâmetros"
          f" {m:12,} multiplicações")
print(f"razão: {parametros(comum) / parametros(separavel):.1f}"
      " vezes menos")
