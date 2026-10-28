"""Vetores de palavras: o skip-gram com amostras negativas."""
import numpy as np
import torch
import torch.nn.functional as F
from torch import nn


def pares(listas, janela=2):
    """Os pares (centro, vizinho) a até `janela` passos."""
    centro, vizinho = [], []
    for ids in listas:
        for i, c in enumerate(ids):
            for j in range(max(0, i - janela),
                           min(len(ids), i + janela + 1)):
                if j != i:
                    centro.append(c)
                    vizinho.append(ids[j])
    return torch.tensor(centro), torch.tensor(vizinho)


class SkipGram(nn.Module):
    def __init__(self, n, dim):
        super().__init__()
        self.centro = nn.Embedding(n, dim)
        self.contexto = nn.Embedding(n, dim)

    def forward(self, c, v, negativos):
        e = self.centro(c)                   # (lote, dim)
        pos = (e * self.contexto(v)).sum(1)  # (lote,)
        neg = self.contexto(negativos) @ e.unsqueeze(2)
        neg = neg.squeeze(2)                 # (lote, k)
        return -(F.logsigmoid(pos)
                 + F.logsigmoid(-neg).sum(1)).mean()


def treina_vetores(voc, textos, dim=32, epocas=15, k=5,
                   lote=512):
    torch.manual_seed(0)
    listas = [voc.codifica(x) for x in textos]
    c, v = pares(listas)
    conta = np.bincount(np.concatenate(listas),
                        minlength=len(voc)).astype(float)
    conta[:2] = 0                    # nada de <pad> e <unk>
    sorteio = torch.tensor(conta ** 0.75)
    modelo = SkipGram(len(voc), dim)
    otimo = torch.optim.Adam(modelo.parameters(), lr=0.005)
    for epoca in range(epocas):
        ordem, total = torch.randperm(len(c)), 0.0
        for i in range(0, len(c), lote):
            j = ordem[i:i + lote]
            neg = torch.multinomial(sorteio, len(j) * k,
                                    replacement=True)
            perda = modelo(c[j], v[j], neg.view(-1, k))
            otimo.zero_grad()
            perda.backward()
            otimo.step()
            total += perda.item() * len(j)
        print(f"época {epoca + 1}: perda {total / len(c):.3f}")
    return modelo.centro.weight.detach().numpy()


def vizinhos(vetores, voc, palavra, n=5):
    """As n palavras de maior cosseno com `palavra`."""
    norma = np.linalg.norm(vetores, axis=1, keepdims=True)
    u = vetores / norma
    cos = u @ u[voc.numero[palavra]]
    cos[:2] = -2                     # fora <pad> e <unk>
    ordem = np.argsort(-cos)[1:n + 1]
    return [(voc.tokens[j], float(cos[j])) for j in ordem]
