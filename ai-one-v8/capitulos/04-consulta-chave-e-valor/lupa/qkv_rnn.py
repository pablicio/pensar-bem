"""O extrator com consulta, chave e valor: três projeções
aprendidas separam os três papéis do estado."""
import math

import torch
from torch import nn

from .extrator import PAD


class ExtratorQKV(nn.Module):
    def __init__(self, n_voc, emb=64, oculto=128, d=64,
                 escala=True):
        super().__init__()
        self.emb = nn.Embedding(n_voc, emb, padding_idx=PAD)
        self.cod = nn.GRU(emb, oculto, batch_first=True)
        self.dec = nn.GRU(emb + d, oculto, batch_first=True)
        self.W_q = nn.Linear(oculto, d, bias=False)
        self.W_k = nn.Linear(oculto, d, bias=False)
        self.W_v = nn.Linear(oculto, d, bias=False)
        self.saida = nn.Linear(oculto + d, n_voc)
        self.divisor = math.sqrt(d) if escala else 1.0
        self.pesos = None

    def forward(self, x, y_in):
        estados, h = self.cod(self.emb(x))
        K = self.W_k(estados)        # chaves: (lote, T, d)
        V = self.W_v(estados)        # valores: (lote, T, d)
        logits, pesos = [], []
        for t in range(y_in.shape[1]):
            q = self.W_q(h[-1])      # consulta: (lote, d)
            notas = torch.einsum("bd,btd->bt", q, K)
            notas = notas / self.divisor
            notas = notas.masked_fill(x == PAD, float("-inf"))
            w = notas.softmax(dim=-1)
            contexto = torch.einsum("bt,btd->bd", w, V)
            entrada = torch.cat([self.emb(y_in[:, t]),
                                 contexto], dim=-1)
            o, h = self.dec(entrada[:, None], h)
            logits.append(self.saida(
                torch.cat([o[:, 0], contexto], dim=-1)))
            pesos.append(w)
        self.pesos = torch.stack(pesos, dim=1)
        return torch.stack(logits, dim=1)
