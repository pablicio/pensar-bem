import numpy as np
import torch

from lupa.atencao_numpy import (atencao, atencao_backward,
                                softmax_vjp)

rng = np.random.default_rng(0)
n, m, d, dv = 3, 5, 4, 2
Q, K = rng.normal(size=(n, d)), rng.normal(size=(m, d))
V = rng.normal(size=(m, dv))
G = rng.normal(size=(n, dv))       # L = soma(O ⊙ G): dL/dO = G


def perda(Q, K, V):
    return (atencao(Q, K, V)[0] * G).sum()


O, P = atencao(Q, K, V)
dQ, dK, dV = atencao_backward(Q, K, V, P, G)


def numerico(X):
    """dL/dX por diferenças finitas centrais."""
    g = np.zeros_like(X)
    for i in np.ndindex(X.shape):
        orig = X[i]
        X[i] = orig + 1e-6
        mais = perda(Q, K, V)
        X[i] = orig - 1e-6
        menos = perda(Q, K, V)
        X[i] = orig
        g[i] = (mais - menos) / 2e-6
    return g


tq, tk, tv = (torch.tensor(a, requires_grad=True)
              for a in (Q, K, V))
saida = torch.softmax(tq @ tk.T / d ** 0.5, dim=-1) @ tv
(saida * torch.tensor(G)).sum().backward()
print("     à mão x numérico   à mão x autograd")
for nome, nosso, X, t in [("dQ", dQ, Q, tq), ("dK", dK, K, tk),
                          ("dV", dV, V, tv)]:
    a = np.abs(nosso - numerico(X)).max()
    b = np.abs(nosso - t.grad.numpy()).max()
    print(f"{nome}   {a:16.1e}   {b:16.1e}")

# cada linha de dS soma zero: o gradiente só mexe nas notas
# umas em relação às outras
dS = softmax_vjp(P, G @ V.T)
print("\nsoma de cada linha de dS:", dS.sum(axis=1).round(15))
