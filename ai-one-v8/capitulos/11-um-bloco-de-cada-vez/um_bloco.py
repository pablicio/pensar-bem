import torch

from lupa.bloco import Bloco

d, h = 64, 4
bloco = Bloco(d, h)
n = sum(p.numel() for p in bloco.parameters())
print("parâmetros do bloco:", n, "| 12d² + 9d =",
      12 * d**2 + 9 * d)
for nome, filho in bloco.named_children():
    m = sum(p.numel() for p in filho.parameters())
    print(f"  {nome:9} {m:7,}")
x = torch.randn(2, 10, d)
print("entrada", tuple(x.shape), "-> saída",
      tuple(bloco(x).shape))
