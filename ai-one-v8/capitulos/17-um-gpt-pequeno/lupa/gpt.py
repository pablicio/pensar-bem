"""Um GPT pequeno, com entrada e saída amarradas."""
import math

import torch
import torch.nn.functional as F
from torch import nn

from .bloco import Bloco


class GPT(nn.Module):
    def __init__(self, V, T=128, d=128, h=4, L=4, dropout=0.1):
        super().__init__()
        self.T = T
        self.emb = nn.Embedding(V, d)
        self.pos = nn.Embedding(T, d)
        self.blocos = nn.ModuleList(
            Bloco(d, h, dropout=dropout) for _ in range(L))
        self.norma = nn.LayerNorm(d)
        self.saida = nn.Linear(d, V, bias=False)
        self.saida.weight = self.emb.weight    # amarrados
        self.apply(self.inicia)
        desvio = 0.02 / math.sqrt(2 * L)       # do GPT-2
        for b in self.blocos:
            nn.init.normal_(b.atencao.W_o.weight, std=desvio)
            nn.init.normal_(b.adiante.desce.weight, std=desvio)

    def inicia(self, m):
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, std=0.02)
        if isinstance(m, nn.Linear) and m.bias is not None:
            nn.init.zeros_(m.bias)

    def forward(self, x, alvo=None):
        T = x.shape[1]
        h = self.emb(x) + self.pos(torch.arange(T))
        futuro = torch.ones(T, T, dtype=torch.bool).triu(1)
        for b in self.blocos:
            h = b(h, futuro)
        logits = self.saida(self.norma(h))
        if alvo is None:
            return logits
        return F.cross_entropy(logits.flatten(0, 1),
                               alvo.flatten())

    @torch.no_grad()
    def gera(self, x, n, escolhe):
        """Acrescenta n tokens a x; escolhe(logits) decide."""
        for _ in range(n):
            logits = self(x[:, -self.T:])[:, -1]
            x = torch.cat([x, escolhe(logits)], dim=1)
        return x


def lote(ids, B, T, gerador=None):
    """B trechos de T tokens, e os mesmos deslocados de um."""
    i = torch.randint(0, len(ids) - T - 1, (B,),
                      generator=gerador)
    x = torch.stack([ids[j:j + T] for j in i])
    y = torch.stack([ids[j + 1:j + T + 1] for j in i])
    return x, y


def taxa(passo, maxima, aquecimento, total):
    """Subida linear, depois cosseno até um décimo."""
    if passo < aquecimento:
        return maxima * (passo + 1) / aquecimento
    fracao = (passo - aquecimento) / (total - aquecimento)
    cosseno = 0.5 * (1 + math.cos(math.pi * fracao))
    return maxima * (0.1 + 0.9 * cosseno)
