import time

import torch

from lupa.corpus import prepara
from lupa.diario import mostra

inicio = time.time()
tok, treino, teste = prepara()
V = len(tok.vocab)
print(f"{len(treino)} tokens de treino, {len(teste)} de teste,"
      f" V = {V} ({time.time() - inicio:.0f} s)")

# C[i, j]: quantas vezes o token j veio depois do token i
C = torch.zeros(V, V)
uns = torch.ones(len(treino) - 1)
C.index_put_((treino[:-1], treino[1:]), uns, accumulate=True)
print(f"pares diferentes: {(C > 0).sum().item()} de {V * V}")


def nll(P, ids):
    """Entropia cruzada média, em bits por token."""
    p = P[ids[:-1], ids[1:]]
    return -(p.log2()).mean().item()


P = C / C.sum(1, keepdim=True).clamp(min=1)
vistos = C[teste[:-1], teste[1:]] > 0
novos = 100 * (~vistos).float().mean()
print(f"pares do teste nunca vistos: {novos:.2f}%")
print(f"treino: {nll(P, treino):.3f} bits por token")

for alfa in [1.0, 0.1, 0.01, 0.001]:
    Pa = (C + alfa) / (C + alfa).sum(1, keepdim=True)
    h = nll(Pa, teste)
    print(f"alfa = {alfa:<6} teste {h:.3f} bits,"
          f" perplexidade {2 ** h:.2f}")

# amostrar um ato, token a token, com alfa = 0.01
Pa = (C + 0.01) / (C + 0.01).sum(1, keepdim=True)
gerador = torch.Generator().manual_seed(1)
i, saida = tok.especial["<|fim|>"], []
for _ in range(60):
    i = torch.multinomial(Pa[i], 1, generator=gerador).item()
    saida.append(i)
print()
mostra(tok.decodifica(saida))
