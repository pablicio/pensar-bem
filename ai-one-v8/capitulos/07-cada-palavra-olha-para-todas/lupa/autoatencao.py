"""Uma cabeça de autoatenção em PyTorch."""
import math

import torch
from torch import nn


class Autoatencao(nn.Module):
    """Cada token olha para todos, ou só para os anteriores
    (causal=True). Consulta, chave e valor vêm do mesmo x."""

    def __init__(self, d_modelo, d, causal=False):
        super().__init__()
        self.W_q = nn.Linear(d_modelo, d, bias=False)
        self.W_k = nn.Linear(d_modelo, d, bias=False)
        self.W_v = nn.Linear(d_modelo, d, bias=False)
        self.causal = causal
        self.pesos = None

    def forward(self, x, preenchido=None):
        """x: (lote, T, d_modelo); preenchido: (lote, T),
        True nas posições de <pad>."""
        q, k, v = self.W_q(x), self.W_k(x), self.W_v(x)
        T = x.shape[1]
        d = q.shape[-1]
        notas = q @ k.transpose(-2, -1) / math.sqrt(d)
        if self.causal:
            futuro = torch.ones(T, T, dtype=torch.bool).triu(1)
            notas = notas.masked_fill(futuro, float("-inf"))
        if preenchido is not None:
            # nenhuma consulta olha para uma chave de <pad>
            notas = notas.masked_fill(preenchido[:, None, :],
                                      float("-inf"))
        self.pesos = notas.softmax(dim=-1)   # (lote, T, T)
        return self.pesos @ v
