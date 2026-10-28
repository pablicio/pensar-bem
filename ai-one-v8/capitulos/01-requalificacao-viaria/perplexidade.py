import math
import re
import unicodedata
from collections import Counter

from lupa.diario import atos

PALAVRA = re.compile(r"\w+[-\w]*|[^\w\s]")


def palavras(texto):
    texto = unicodedata.normalize("NFC", texto)
    texto = texto.replace("-\n", "")
    return ["<ato>"] + PALAVRA.findall(texto)


corpus = atos()
treino = [palavras(a["texto"]) for a in corpus
          if a["data"] < "2027-01-01"]
teste = [palavras(a["texto"]) for a in corpus
         if a["data"] >= "2027-01-01"]
conta = Counter(p for ato in treino for p in ato)
vocab = {p for p, n in conta.items() if n >= 2} | {"<?>"}


def troca(ato):
    return [p if p in vocab else "<?>" for p in ato]


treino = [troca(a) for a in treino]
teste = [troca(a) for a in teste]
uni = Counter(p for ato in treino for p in ato)
bi = Counter(par for ato in treino
             for par in zip(ato, ato[1:]))
total = sum(uni.values())


def p_uni(w):
    return uni[w] / total


def p_bi(v, w, lam=0.9):
    """O bigrama misturado com o unigrama: nunca dá zero."""
    return lam * bi[(v, w)] / uni[v] + (1 - lam) * p_uni(w)


bits_uni = bits_bi = 0.0
n = 0
for ato in teste:
    for v, w in zip(ato, ato[1:]):
        bits_uni -= math.log2(p_uni(w))
        bits_bi -= math.log2(p_bi(v, w))
        n += 1
print(f"{len(vocab):,} palavras no vocabulário,"
      f" {n:,} palavras de teste")
h = math.log2(len(vocab))
print(f"uniforme: {h:5.2f} bits por palavra,"
      f" perplexidade {len(vocab):8,.1f}")
for nome, bits in [("unigrama", bits_uni),
                   ("bigrama", bits_bi)]:
    h = bits / n
    print(f"{nome:9}: {h:5.2f} bits por palavra,"
          f" perplexidade {2 ** h:8,.1f}")

nova = next(a for a in corpus if "eixo central" in a["texto"])
ps = troca(palavras(nova["texto"]))
i = ps.index("Objeto")
print("\na surpresa de cada palavra, em bits:")
for v, w in zip(ps[i:i + 14], ps[i + 1:i + 15]):
    print(f"  {w:16} {-math.log2(p_bi(v, w)):5.1f}")
