"""O extrator com atenção: a cada palavra que escreve, o
decodificador consulta todos os estados do codificador."""
import torch
from torch import nn

from .extrator import PAD


class ExtratorComAtencao(nn.Module):
    def __init__(self, n_voc, emb=64, oculto=128):
        super().__init__()
        self.emb = nn.Embedding(n_voc, emb, padding_idx=PAD)
        self.cod = nn.GRU(emb, oculto, batch_first=True)
        self.dec = nn.GRU(emb + oculto, oculto,
                          batch_first=True)
        self.saida = nn.Linear(2 * oculto, n_voc)
        self.pesos = None        # os pesos da última chamada

    def forward(self, x, y_in):
        # todos os estados, (lote, T, oculto), e o último
        estados, h = self.cod(self.emb(x))
        logits, pesos = [], []
        for t in range(y_in.shape[1]):
            g = h[-1]               # a pergunta (lote, oculto)
            notas = torch.einsum("bh,bth->bt", g, estados)
            notas = notas.masked_fill(x == PAD, float("-inf"))
            w = notas.softmax(dim=-1)     # os pesos: (lote, T)
            contexto = torch.einsum("bt,bth->bh", w, estados)
            entrada = torch.cat([self.emb(y_in[:, t]),
                                 contexto], dim=-1)
            o, h = self.dec(entrada[:, None], h)
            logits.append(self.saida(
                torch.cat([o[:, 0], contexto], dim=-1)))
            pesos.append(w)
        self.pesos = torch.stack(pesos, dim=1)  # (lote, S, T)
        return torch.stack(logits, dim=1)
