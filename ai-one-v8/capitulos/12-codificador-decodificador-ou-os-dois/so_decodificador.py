import torch
import torch.nn.functional as F
from torch import nn

from lupa.bloco import Bloco
from lupa.posicao import senoidal
from lupa.tradutor import pares

torch.manual_seed(0)
treino, teste = pares(8000, semente=1), pares(1000, semente=2)
# um vocabulário só: palavras, o separador e os caracteres
palavras = sorted({p for e, _ in treino for p in e})
simbolos = ["<pad>", "="] + palavras + list("0123456789-")
idx = {s: i for i, s in enumerate(simbolos)}


class SoDecodificador(nn.Module):
    """A entrada, um "=" e a saída, numa sequência só, com a
    máscara causal: o desenho do GPT."""

    def __init__(self, n, d=64, h=4, L=4):
        super().__init__()
        self.d = d
        self.emb = nn.Embedding(n, d)
        self.blocos = nn.ModuleList(Bloco(d, h)
                                    for _ in range(L))
        self.norma = nn.LayerNorm(d)
        self.saida = nn.Linear(d, n)

    def forward(self, x):
        T = x.shape[1]
        h = self.emb(x) + senoidal(T, self.d)
        futuro = torch.ones(T, T, dtype=torch.bool).triu(1)
        for b in self.blocos:
            h = b(h, futuro)
        return self.saida(self.norma(h))


def lote(ps):
    """A entrada alinhada à direita, para o '=' cair sempre na
    mesma coluna; o preenchimento fica à esquerda."""
    E = max(len(e) for e, _ in ps)
    x = torch.zeros(len(ps), E + 1 + 10, dtype=torch.long)
    for i, (e, s) in enumerate(ps):
        seq = [idx[p] for p in e] + [idx["="]]
        seq += [idx[c] for c in s]
        x[i, E - len(e):] = torch.tensor(seq)
    return x, E


m = SoDecodificador(len(simbolos))
print(sum(p.numel() for p in m.parameters()), "parâmetros")
opt = torch.optim.Adam(m.parameters(), lr=1e-3)
for epoca in range(8):
    for k in range(0, len(treino), 64):
        x, E = lote(treino[k:k + 64])
        logits = m(x[:, :-1])[:, E:]          # depois do "="
        perda = F.cross_entropy(logits.flatten(0, 1),
                                x[:, E + 1:].flatten())
        opt.zero_grad()
        perda.backward()
        opt.step()
print(f"perda final {perda.item():.4f}")

with torch.no_grad():
    x, E = lote(teste)
    y = x[:, :E + 1]                          # até o "="
    for _ in range(10):
        proximo = m(y)[:, -1].argmax(-1, keepdim=True)
        y = torch.cat([y, proximo], dim=1)
certas = (y[:, E + 1:] == x[:, E + 1:]).all(dim=1)
print(f"datas do teste sem erro: {certas.float().mean():.1%}")
