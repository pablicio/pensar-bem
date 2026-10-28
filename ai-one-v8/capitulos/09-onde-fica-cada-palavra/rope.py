import torch

from lupa.posicao import frequencias, rope

torch.manual_seed(0)
T, d = 50, 8
q = torch.randn(d).expand(T, d)          # a mesma consulta...
k = torch.randn(d).expand(T, d)          # ...e a mesma chave
Q, K = rope(q), rope(k)                  # em todas as posições
notas = Q @ K.T
# a nota de (t, s) só depende de t - s
print("(3, 1) e (40, 38):", f"{notas[3, 1]:.4f}",
      f"{notas[40, 38]:.4f}")
print("(1, 3) e (38, 40):", f"{notas[1, 3]:.4f}",
      f"{notas[38, 40]:.4f}")

# a mesma rotação, com números complexos
pares = q.reshape(T, d // 2, 2).contiguous()
zq = torch.view_as_complex(pares)
giro = torch.polar(torch.ones(T, d // 2),
                   torch.arange(T)[:, None] * frequencias(d))
Qc = torch.view_as_real(zq * giro).reshape(T, d)
print("rope() = multiplicar por e^(itω):",
      f"{(Qc - Q).abs().max():.1e}")
