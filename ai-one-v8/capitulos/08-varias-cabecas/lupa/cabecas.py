"""Atenção com várias cabeças."""
import math

from torch import nn


class VariasCabecas(nn.Module):
    """h cabeças de dimensão d_modelo / h, cada uma com a sua
    softmax, juntadas e misturadas por W_o."""

    def __init__(self, d_modelo, h):
        super().__init__()
        assert d_modelo % h == 0
        self.h, self.d = h, d_modelo // h
        self.W_q = nn.Linear(d_modelo, d_modelo, bias=False)
        self.W_k = nn.Linear(d_modelo, d_modelo, bias=False)
        self.W_v = nn.Linear(d_modelo, d_modelo, bias=False)
        self.W_o = nn.Linear(d_modelo, d_modelo, bias=False)
        self.pesos = None

    def separa(self, x):
        """(lote, T, d_modelo) -> (lote, h, T, d)"""
        lote, T, _ = x.shape
        return x.view(lote, T, self.h, self.d).transpose(1, 2)

    def forward(self, x_q, x_kv, mascara=None):
        """mascara: True onde não se pode olhar, num formato
        que o broadcasting leve a (lote, h, Tq, Tkv)."""
        q = self.separa(self.W_q(x_q))
        k = self.separa(self.W_k(x_kv))
        v = self.separa(self.W_v(x_kv))
        notas = q @ k.transpose(-2, -1) / math.sqrt(self.d)
        if mascara is not None:
            notas = notas.masked_fill(mascara, float("-inf"))
        self.pesos = notas.softmax(dim=-1)  # lote, h, Tq, Tkv
        o = self.pesos @ v                  # (lote, h, Tq, d)
        lote, _, Tq, _ = o.shape
        o = o.transpose(1, 2).reshape(lote, Tq, -1)  # junta
        return self.W_o(o)
