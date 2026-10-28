"""Normalização, pré-tokenização e BPE: um tokenizador."""
import re
from collections import Counter

from lupa.bpe import BPE, funde
from lupa.extrator import limpa

# letras (com o espaço da frente), um dígito, pontuação,
# espaços
PEDACO = re.compile(r" ?[^\W\d_]+| ?\d| ?(?:[^\w\s]|_)+"
                    r"|\s+(?!\S)|\s+")
ESPECIAIS = ["<|fim|>"]


class Tokenizador(BPE):
    def __init__(self):
        super().__init__()
        self.cache = {}                      # pedaço -> tokens

    def treina(self, textos, V):
        # cada pedaço diferente uma vez, com a sua contagem
        contagem = Counter(p for t in textos
                           for p in PEDACO.findall(limpa(t)))
        pedacos = {tuple(p.encode("utf-8")): n
                   for p, n in contagem.items()}
        for novo in range(256, V - len(ESPECIAIS)):
            pares = Counter()
            for ids, n in pedacos.items():
                for par in zip(ids, ids[1:]):
                    pares[par] += n
            par = max(pares, key=pares.get)
            pedacos = {tuple(funde(list(ids), par, novo)): n
                       for ids, n in pedacos.items()}
            self.fusoes[par] = novo
            a, b = par
            self.vocab[novo] = self.vocab[a] + self.vocab[b]
        primeiro = V - len(ESPECIAIS)
        self.especial = {s: primeiro + i
                         for i, s in enumerate(ESPECIAIS)}
        for s, i in self.especial.items():
            self.vocab[i] = s.encode("utf-8")

    def codifica(self, texto):
        ids = []
        for parte in re.split(r"(<\|fim\|>)", texto):
            if parte in self.especial:
                ids.append(self.especial[parte])
                continue
            for p in PEDACO.findall(limpa(parte)):
                if p not in self.cache:
                    self.cache[p] = super().codifica(p)
                ids += self.cache[p]
        return ids
