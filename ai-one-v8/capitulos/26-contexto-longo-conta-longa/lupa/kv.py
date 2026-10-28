"""Gerar com o cache de chaves e valores, no GPT pequeno."""
import math

import torch


@torch.no_grad()
def passo(modelo, token, t, cache):
    """Os logits do token na posição t, guardando k e v.
    cache: uma lista (K, V) por bloco, que cresce."""
    h = modelo.emb(token) + modelo.pos.weight[t]     # (1, d)
    for b, (K, V) in zip(modelo.blocos, cache):
        at = b.atencao
        a = b.norma1(h)
        q = at.W_q(a).view(at.h, 1, at.d)           # (h, 1, d)
        K.append(at.W_k(a).view(at.h, 1, at.d))
        V.append(at.W_v(a).view(at.h, 1, at.d))
        k, v = torch.cat(K, 1), torch.cat(V, 1)  # (h, t+1, d)
        pesos = q @ k.transpose(1, 2) / math.sqrt(at.d)
        o = pesos.softmax(-1) @ v                   # (h, 1, d)
        h = h + at.W_o(o.transpose(0, 1).reshape(1, -1))
        h = h + b.adiante(b.norma2(h))
    return modelo.saida(modelo.norma(h))[0]


@torch.no_grad()
def gera(modelo, ids, n):
    """Escolha gulosa, um token por passo, com o cache."""
    cache = [([], []) for _ in modelo.blocos]
    for t, i in enumerate(ids[:-1]):                 # o começo
        passo(modelo, torch.tensor([i]), t, cache)
    saida = list(ids)
    for t in range(len(ids) - 1, len(ids) - 1 + n):
        ultimo = torch.tensor([saida[-1]])
        logits = passo(modelo, ultimo, t, cache)
        saida.append(logits.argmax().item())
    return saida
