import re
import unicodedata
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from lupa.diario import atos


def limpa(t):
    return unicodedata.normalize("NFC", t).replace("-\n", "")


PALAVRA = re.compile(r"\w+|[^\w\s]")
PALAVRA_DIGITO = re.compile(r"\d|[^\W\d]+|[^\w\s]")
UNIDADES = {
    "bytes": lambda t: list(t.encode("utf-8")),
    "caracteres": lambda t: list(limpa(t)),
    "palavras": lambda t: PALAVRA.findall(limpa(t)),
    "palavras, dígitos 1 a 1": lambda t:
        PALAVRA_DIGITO.findall(limpa(t)),
}
corpus = atos()
treino = [a["texto"] for a in corpus if a["data"] < "2027"]
teste = [a["texto"] for a in corpus if a["data"] >= "2027"]

cabeca = ["vocab.", "únicos", "novos", "por ato"]
print(f"{'unidade':24}" + "".join(f"{c:>8}" for c in cabeca))
for nome, quebra in UNIDADES.items():
    conta = Counter(u for t in treino for u in quebra(t))
    unicos = sum(n == 1 for n in conta.values()) / len(conta)
    toks = [quebra(t) for t in teste]
    novos = sum(u not in conta for ts in toks for u in ts)
    total = sum(len(ts) for ts in toks)
    print(f"{nome:24} {len(conta):8,} {unicos:8.0%}"
          f" {novos / total:8.2%} {total / len(toks):8.0f}")

# a lei de Zipf: frequência contra posição no ranking
conta = Counter(u for t in treino
                for u in PALAVRA.findall(limpa(t)))
freq = np.array(sorted(conta.values(), reverse=True), float)
rank = np.arange(1, len(freq) + 1)
faixa = slice(9, 1000)                 # posições 10 a 1000
a, b = np.polyfit(np.log(rank[faixa]), np.log(freq[faixa]), 1)
print(f"\nZipf: log f = {a:.2f} log r + {b:.2f}")
print("as dez mais frequentes:",
      " ".join(p for p, _ in conta.most_common(10)))

fig, eixo = plt.subplots(figsize=(6, 3))
eixo.loglog(rank, freq, ".", markersize=2)
eixo.loglog(rank[faixa], np.exp(b) * rank[faixa] ** a, "-")
eixo.set_xlabel("posição no ranking")
eixo.set_ylabel("ocorrências")
fig.tight_layout()
fig.savefig("zipf.png", dpi=300)
