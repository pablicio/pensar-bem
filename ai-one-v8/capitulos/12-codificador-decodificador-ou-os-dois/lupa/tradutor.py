"""O Transformer de 2017, com codificador e decodificador."""
import random
from datetime import date, timedelta

import torch
from torch import nn

from dados.extenso import data_por_extenso

from .bloco import Bloco, RedeAdiante
from .cabecas import VariasCabecas
from .posicao import senoidal


def pares(n, semente):
    """(data por extenso, data no formato ISO), sorteadas entre
    2000 e 2035."""
    rng = random.Random(semente)
    inicio = date(2000, 1, 1)
    lista = []
    for _ in range(n):
        d = inicio + timedelta(days=rng.randrange(13149))
        lista.append((data_por_extenso(d).split(),
                      list(d.isoformat())))
    return lista


class BlocoDecodificador(nn.Module):
    """Autoatenção causal, atenção cruzada e rede adiante."""

    def __init__(self, d, h):
        super().__init__()
        self.norma1 = nn.LayerNorm(d)
        self.auto = VariasCabecas(d, h)
        self.norma2 = nn.LayerNorm(d)
        self.cruzada = VariasCabecas(d, h)
        self.norma3 = nn.LayerNorm(d)
        self.adiante = RedeAdiante(d)

    def forward(self, y, memoria, futuro, pad_memoria):
        a = self.norma1(y)
        y = y + self.auto(a, a, futuro)
        # as consultas vêm do decodificador; chaves e valores,
        # da saída do codificador
        b = self.norma2(y)
        y = y + self.cruzada(b, memoria, pad_memoria)
        return y + self.adiante(self.norma3(y))


class Tradutor(nn.Module):
    def __init__(self, n_entrada, n_saida, d=64, h=4, L=2):
        super().__init__()
        self.d = d
        self.emb_ent = nn.Embedding(n_entrada, d,
                                    padding_idx=0)
        self.emb_sai = nn.Embedding(n_saida, d)
        self.cod = nn.ModuleList(Bloco(d, h) for _ in range(L))
        self.dec = nn.ModuleList(BlocoDecodificador(d, h)
                                 for _ in range(L))
        self.norma_cod = nn.LayerNorm(d)
        self.norma_dec = nn.LayerNorm(d)
        self.saida = nn.Linear(d, n_saida)

    def codifica(self, x):
        e = self.emb_ent(x) + senoidal(x.shape[1], self.d)
        pad = (x == 0)[:, None, None, :]   # (lote, 1, 1, T)
        for bloco in self.cod:
            e = bloco(e, pad)
        return self.norma_cod(e), pad

    def forward(self, x, y_in):
        memoria, pad = self.codifica(x)
        S = y_in.shape[1]
        y = self.emb_sai(y_in) + senoidal(S, self.d)
        futuro = torch.ones(S, S, dtype=torch.bool).triu(1)
        for bloco in self.dec:
            y = bloco(y, memoria, futuro, pad)
        return self.saida(self.norma_dec(y))
