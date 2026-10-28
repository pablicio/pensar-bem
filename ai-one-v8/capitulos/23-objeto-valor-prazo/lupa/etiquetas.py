"""Etiquetas BIO: em que trecho do ato está cada entidade."""
import torch
from torch import nn

from .extrator import limpa
from .mlm import especiais
from .tokenizador import PEDACO

ENTIDADES = ["CONTRATADA", "OBJETO", "VALOR", "PRAZO"]
ROTULOS = ["O"] + [f"{p}-{e}" for e in ENTIDADES for p in "BI"]


def tokens_e_posicoes(tok, texto):
    """Os tokens do texto limpo e os bytes de cada um."""
    limpo = limpa(texto)
    ids, posicoes = [], []
    for m in PEDACO.finditer(limpo):
        b = len(limpo[:m.start()].encode("utf-8"))
        for i in tok.codifica(m.group()):
            n = len(tok.vocab[i])
            espaco = tok.vocab[i].startswith(b" ")
            # o trecho do token, sem o espaço da frente
            posicoes.append((b + espaco, b + n))
            ids.append(i)
            b += n
    return ids, posicoes


def em_bytes(texto, inicio, fim):
    """Um trecho do texto cru, em bytes do texto limpo."""
    a = len(limpa(texto[:inicio]).encode("utf-8"))
    b = len(limpa(texto[:fim]).encode("utf-8"))
    return a, b


def etiqueta(posicoes, trechos):
    """B- no primeiro token de cada entidade, I- nos outros."""
    rotulos = []
    for ini, fim in posicoes:
        r = "O"
        for a, b, nome in trechos:
            if a <= ini < b:
                dentro = rotulos and rotulos[-1].endswith(nome)
                r = ("I-" if dentro else "B-") + nome
        rotulos.append(r)
    return rotulos


def trechos_bio(rotulos):
    """De volta: (nome, primeiro token, último + 1)."""
    achados, aberto = set(), None
    for i, r in enumerate(rotulos + ["O"]):
        if aberto and not r == "I-" + aberto[0]:
            achados.add((aberto[0], aberto[1], i))
            aberto = None
        if r.startswith("B-"):
            aberto = (r[2:], i)
    return achados


class Etiquetador(nn.Module):
    """Uma camada linear sobre o estado de cada token."""

    def __init__(self, bert, d=128):
        super().__init__()
        self.bert = bert
        self.cabeca = nn.Linear(d, len(ROTULOS))

    def forward(self, ids, vazio):
        return self.cabeca(self.bert(ids, vazio))


def tensores(exemplos, V, T=128):
    """[CLS] + tokens; alvo -100 no [CLS] e no [PAD]."""
    CLS, PAD = especiais(V)["[CLS]"], especiais(V)["[PAD]"]
    ids = torch.full((len(exemplos), T), PAD)
    alvo = torch.full((len(exemplos), T), -100)
    for k, (x, r) in enumerate(exemplos):
        x, r = x[:T - 1], r[:T - 1]
        ids[k, 0] = CLS
        ids[k, 1:len(x) + 1] = torch.tensor(x)
        alvo[k, 1:len(r) + 1] = torch.tensor(
            [ROTULOS.index(e) for e in r])
    return ids, ids == PAD, alvo
