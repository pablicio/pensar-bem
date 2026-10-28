"""O bloco Transformer: atenção e rede alimentada adiante,
cada uma com conexão residual e normalização de camada."""
import math

import torch
from torch import nn

from .cabecas import VariasCabecas


class RedeAdiante(nn.Module):
    """d -> 4d -> d, com GELU no meio."""

    def __init__(self, d, fator=4, dropout=0.0):
        super().__init__()
        self.sobe = nn.Linear(d, fator * d)
        self.desce = nn.Linear(fator * d, d)
        self.gelu = nn.GELU()
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        meio = self.gelu(self.sobe(x))
        return self.dropout(self.desce(meio))


class Bloco(nn.Module):
    def __init__(self, d, h, pre=True, dropout=0.0):
        super().__init__()
        self.norma1 = nn.LayerNorm(d)
        self.atencao = VariasCabecas(d, h)
        self.norma2 = nn.LayerNorm(d)
        self.adiante = RedeAdiante(d, dropout=dropout)
        self.dropout = nn.Dropout(dropout)
        self.pre = pre

    def forward(self, x, mascara=None):
        if self.pre:     # normaliza a entrada de cada ramo
            a = self.norma1(x)
            x = x + self.dropout(self.atencao(a, a, mascara))
            x = x + self.adiante(self.norma2(x))
        else:            # normaliza a soma, como em 2017
            x = self.norma1(
                x + self.dropout(self.atencao(x, x, mascara)))
            x = self.norma2(x + self.adiante(x))
        return x


class Pilha(nn.Module):
    """L blocos causais sobre caracteres: um modelo de
    linguagem mínimo, para medir o bloco."""

    def __init__(self, n_voc, L, d=64, h=4, T=128, pre=True,
                 escala=False):
        super().__init__()
        self.emb = nn.Embedding(n_voc, d)
        self.pos = nn.Embedding(T, d)
        self.blocos = nn.ModuleList(Bloco(d, h, pre)
                                    for _ in range(L))
        self.norma = nn.LayerNorm(d) if pre else nn.Identity()
        self.saida = nn.Linear(d, n_voc)
        if escala:       # a inicialização do GPT-2
            desvio = 0.02 / math.sqrt(2 * L)
            for b in self.blocos:
                for w in (b.atencao.W_o.weight,
                          b.adiante.desce.weight):
                    nn.init.normal_(w, std=desvio)

    def forward(self, x, fluxo=None):
        T = x.shape[1]
        h = self.emb(x) + self.pos(torch.arange(T))
        futuro = torch.ones(T, T, dtype=torch.bool).triu(1)
        for b in self.blocos:
            h = b(h, futuro)
            if fluxo is not None:
                fluxo.append(h.std().item())
        return self.saida(self.norma(h))
