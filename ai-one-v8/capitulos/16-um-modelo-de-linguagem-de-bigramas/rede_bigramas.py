import time

import torch
import torch.nn.functional as F

from lupa.corpus import prepara

tok, treino, teste = prepara()
V, N = len(tok.vocab), len(treino) - 1
C = torch.zeros(V, V)
C.index_put_((treino[:-1], treino[1:]), torch.ones(N),
             accumulate=True)
Ni = C.sum(1, keepdim=True)


def perda(W):
    """A entropia cruzada do corpus, pelas contagens."""
    return -(C * F.log_softmax(W, dim=1)).sum() / N


def bits(P, ids):
    return -P[ids[:-1], ids[1:]].log2().mean().item()


# 1. o gradiente: (N_i p_ij - C_ij) / N
_ = torch.manual_seed(0)
W = torch.randn(V, V, requires_grad=True)
perda(W).backward()
formula = (Ni * F.softmax(W.detach(), dim=1) - C) / N
print("gradiente: autograd - fórmula =",
      f"{(W.grad - formula).abs().max().item():.1e}")

# 2. treinar a tabela de logits por gradiente
for decaimento in [0.0, 1e-7, 1e-6]:
    W = torch.zeros(V, V, requires_grad=True)
    opt = torch.optim.Adam([W], lr=0.5)
    inicio = time.time()
    for passo in range(300):
        L = perda(W) + decaimento * (W ** 2).sum()
        opt.zero_grad()
        L.backward()
        opt.step()
    P = F.softmax(W.detach(), dim=1)
    h_tr, h_te = bits(P, treino), bits(P, teste)
    print(f"decaimento {decaimento:g}: treino {h_tr:.3f},"
          f" teste {h_te:.3f} bits"
          f" ({time.time() - inicio:.0f} s)")
    if decaimento == 0:
        frequentes = Ni.squeeze() > 1000
        dif = (P - C / Ni.clamp(min=1))[frequentes].abs().max()
        print(f"  linhas com mais de mil ocorrências:"
              f" |P - C/N_i| <= {dif.item():.1e}")
