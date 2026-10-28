import torch
from torch import nn

from lupa.cabecas import VariasCabecas

torch.manual_seed(0)
lote, T, d_modelo, h = 2, 5, 16, 4
x = torch.randn(lote, T, d_modelo)
mha = VariasCabecas(d_modelo, h)

q = mha.W_q(x)
print("x:                ", tuple(x.shape))
print("q = x W_q:        ", tuple(q.shape))
print("q separada:       ", tuple(mha.separa(q).shape))
saida = mha(x, x)
print("pesos:            ", tuple(mha.pesos.shape))
print("saída:            ", tuple(saida.shape))
n = sum(p.numel() for p in mha.parameters())
print(f"parâmetros: {n} = 4 · {d_modelo}²")

# a mesma camada do PyTorch, com os mesmos pesos
ref = nn.MultiheadAttention(d_modelo, h, bias=False,
                            batch_first=True)
with torch.no_grad():
    ref.in_proj_weight.copy_(torch.cat(
        [mha.W_q.weight, mha.W_k.weight, mha.W_v.weight]))
    ref.out_proj.weight.copy_(mha.W_o.weight)
saida_ref, _ = ref(x, x, x)
print(f"diferença para nn.MultiheadAttention:"
      f" {(saida - saida_ref).abs().max():.1e}")
