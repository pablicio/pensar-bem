"""Um BERT pequeno: os blocos do GPT sem a máscara causal."""
import math

import torch
import torch.nn.functional as F
from torch import nn

from .bloco import Bloco
from .cabecas import VariasCabecas
from .posicao import rope


class AtencaoRope(VariasCabecas):
    """A atenção do capítulo 8, com q e k girados (RoPE)."""

    def forward(self, x_q, x_kv, mascara=None):
        q = rope(self.separa(self.W_q(x_q)))
        k = rope(self.separa(self.W_k(x_kv)))
        v = self.separa(self.W_v(x_kv))
        notas = q @ k.transpose(-2, -1) / math.sqrt(self.d)
        if mascara is not None:
            notas = notas.masked_fill(mascara, float("-inf"))
        self.pesos = notas.softmax(dim=-1)
        o = self.pesos @ v
        lote, _, T, _ = o.shape
        return self.W_o(o.transpose(1, 2).reshape(lote, T, -1))


class BERT(nn.Module):
    def __init__(self, V, T=128, d=128, h=4, L=4,
                 posicao="rope"):
        super().__init__()
        self.emb = nn.Embedding(V + 3, d)     # + 3 especiais
        aprendida = posicao == "aprendida"
        self.pos = nn.Embedding(T, d) if aprendida else None
        self.blocos = nn.ModuleList(Bloco(d, h)
                                    for _ in range(L))
        if posicao == "rope":
            for b in self.blocos:
                b.atencao = AtencaoRope(d, h)
        self.norma = nn.LayerNorm(d)
        self.saida = nn.Linear(d, V + 3, bias=False)
        self.saida.weight = self.emb.weight
        for m in self.modules():
            if isinstance(m, (nn.Linear, nn.Embedding)):
                nn.init.normal_(m.weight, std=0.02)

    def forward(self, x, vazio=None):
        """Os estados de cada token; vazio marca o [PAD]."""
        h = self.emb(x)
        if self.pos is not None:
            h = h + self.pos(torch.arange(x.shape[1]))
        # (lote, T) -> (lote, 1, 1, T): ninguém olha o vazio
        mascara = (None if vazio is None
                   else vazio[:, None, None])
        for b in self.blocos:
            h = b(h, mascara)
        return self.norma(h)

    def perda_mlm(self, x, alvo):
        logits = self.saida(self(x))
        return F.cross_entropy(logits.flatten(0, 1),
                               alvo.flatten(),
                               ignore_index=-100)
