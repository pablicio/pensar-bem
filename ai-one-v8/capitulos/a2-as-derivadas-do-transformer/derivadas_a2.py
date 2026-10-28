import math

import torch
import torch.nn.functional as F

torch.set_default_dtype(torch.float64)
_ = torch.manual_seed(0)
T, d = 6, 8


def confere(nome, manual, auto):
    erro = (manual - auto).abs().max().item()
    print(f"{nome:28} {erro:.1e}")


# 1. softmax com entropia cruzada: dL/dz = p - y
z = torch.randn(T, 10, requires_grad=True)
y = torch.randint(0, 10, (T,))
F.cross_entropy(z, y, reduction="sum").backward()
p = z.detach().softmax(-1)
confere("entropia cruzada", p - torch.eye(10)[y], z.grad)

# 2. a atenção: S = Q K^T / raiz(d), P = softmax(S), O = P V
Q, K, V = (torch.randn(T, d, requires_grad=True)
           for _ in range(3))
dO = torch.randn(T, d)
S = Q @ K.T / math.sqrt(d)
P = S.softmax(-1)
(P @ V).backward(dO)
P = P.detach()
dV = P.T @ dO
dP = dO @ V.detach().T
dS = P * (dP - (dP * P).sum(-1, keepdim=True))
confere("atenção, dV", dV, V.grad)
confere("atenção, dQ", dS @ K.detach() / math.sqrt(d), Q.grad)
confere("atenção, dK", dS.T @ Q.detach() / math.sqrt(d),
        K.grad)

# 3. normalização de camada: y = g * (x - mu) / sigma + b
x = torch.randn(T, d, requires_grad=True)
g = torch.randn(d, requires_grad=True)
dy = torch.randn(T, d)
ln = F.layer_norm(x, (d,), g, None, eps=1e-5)
ln.backward(dy)
mu = x.detach().mean(-1, keepdim=True)
sigma = (x.detach().var(-1, unbiased=False, keepdim=True)
         + 1e-5).sqrt()
xh = (x.detach() - mu) / sigma
dxh = dy * g.detach()
dx = (dxh - dxh.mean(-1, keepdim=True)
      - xh * (dxh * xh).mean(-1, keepdim=True)) / sigma
confere("normalização, dx", dx, x.grad)
confere("normalização, dg", (dy * xh).sum(0), g.grad)

# 4. GELU exata: x Phi(x), derivada Phi(x) + x phi(x)
u = torch.randn(T, d, requires_grad=True)
F.gelu(u).sum().backward()
Phi = 0.5 * (1 + torch.erf(u.detach() / math.sqrt(2)))
phi = torch.exp(-u.detach() ** 2 / 2) / math.sqrt(2 * math.pi)
confere("GELU", Phi + u.detach() * phi, u.grad)

# 5. camada linear: y = x W^T + b
W = torch.randn(4, d, requires_grad=True)
xl = torch.randn(T, d, requires_grad=True)
dyl = torch.randn(T, 4)
(xl @ W.T).backward(dyl)
confere("linear, dW", dyl.T @ xl.detach(), W.grad)
confere("linear, dx", dyl @ W.detach(), xl.grad)
