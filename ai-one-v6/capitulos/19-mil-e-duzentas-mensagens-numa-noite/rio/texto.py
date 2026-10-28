"""As mensagens do canal como sequências de tokens."""
import re
import unicodedata
from collections import Counter

import pandas as pd

ARQUIVO = "dados/brutos/mensagens.csv"
CLASSES = ["risco", "ajuda", "info", "boato"]
PARTES = {"treino": (2016, 2021), "validacao": (2022, 2022),
          "teste": (2023, 2027)}


def mensagens():
    return pd.read_csv(ARQUIVO, parse_dates=["data_hora"],
                       keep_default_na=False)


def parte(tab, nome):
    inicio, fim = PARTES[nome]
    ano = tab["data_hora"].dt.year
    return tab[(ano >= inicio) & (ano <= fim)]


def normaliza(texto):
    """Minúsculas e sem acento: 'Água' e 'agua' viram um só."""
    nfd = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in nfd
                   if unicodedata.category(c) != "Mn")


def palavras(texto):
    """Palavras, '!' e '?'; todo número vira '<num>'."""
    tokens = re.findall(r"[a-z]+|\d+|[!?]", normaliza(texto))
    return ["<num>" if t.isdigit() else t for t in tokens]


def caracteres(texto):
    return list(normaliza(texto))


class Vocabulario:
    """Token -> número (0: preenchimento, 1: desconhecido)."""

    def __init__(self, textos, separa, minimo=2):
        conta = Counter(t for x in textos for t in separa(x))
        bons = [t for t, n in conta.items() if n >= minimo]
        bons.sort(key=lambda t: (-conta[t], t))
        self.tokens = ["<pad>", "<unk>"] + bons
        self.numero = {t: i
                       for i, t in enumerate(self.tokens)}
        self.separa = separa

    def __len__(self):
        return len(self.tokens)

    def codifica(self, texto):
        return [self.numero.get(t, 1)
                for t in self.separa(texto)]

    def decodifica(self, numeros):
        return " ".join(self.tokens[i] for i in numeros)
