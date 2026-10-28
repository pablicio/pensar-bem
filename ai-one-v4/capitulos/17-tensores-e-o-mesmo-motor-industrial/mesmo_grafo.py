import numpy as np
import torch

from motor.valor import Valor

sorteio = np.random.default_rng(0)
W1, b1 = sorteio.normal(size=(3, 2)), sorteio.normal(size=3)
w2, b2 = sorteio.normal(size=3), sorteio.normal()
x, y = [0.5, -1.2], 1.0

# o motor do capítulo 9
V1 = [[Valor(v) for v in linha] for linha in W1]
c1 = [Valor(v) for v in b1]
v2, c2 = [Valor(v) for v in w2], Valor(b2)
h = [(sum((w * xi for w, xi in zip(linha, x)), b)).tanh()
     for linha, b in zip(V1, c1)]
saida = sum((w * hi for w, hi in zip(v2, h)), c2)
perda = (saida - y) ** 2
perda.backward()

# o PyTorch, em 64 bits
T1 = torch.tensor(W1, requires_grad=True)
d1 = torch.tensor(b1, requires_grad=True)
t2 = torch.tensor(w2, requires_grad=True)
d2 = torch.tensor(b2, dtype=torch.float64, requires_grad=True)
ht = torch.tanh(T1 @ torch.tensor(x, dtype=torch.float64) + d1)
perda_t = (t2 @ ht + d2 - y) ** 2
perda_t.backward()

print(f"perda: motor {perda.dado:.10f},"
      f" PyTorch {perda_t.item():.10f}")
pares = [(V1[i][j].grad, T1.grad[i, j].item())
         for i in range(3) for j in range(2)]
pares += [(v.grad, g.item()) for v, g in zip(v2, t2.grad)]
pares += [(c.grad, g.item()) for c, g in zip(c1, d1.grad)]
pares.append((c2.grad, d2.grad.item()))
dif = max(abs(a - b) for a, b in pares)
print(f"{len(pares)} gradientes; maior diferença: {dif:.1e}")
print("dperda/dW1 pelo PyTorch:")
print(T1.grad.numpy().round(7))
