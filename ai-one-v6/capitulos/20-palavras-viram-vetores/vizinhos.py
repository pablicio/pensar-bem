from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from rio.texto import Vocabulario, mensagens, palavras, parte
from rio.vetores import vizinhos

treino = parte(mensagens(), "treino")["texto"]
voc = Vocabulario(treino, palavras)
vetores = np.load("vetores.npy")
for palavra in ["agua", "auga", "tres", "socorro", "barragem",
                "encheu", "alagada"]:
    perto = vizinhos(vetores, voc, palavra, n=4)
    print(f"{palavra:9}", " ".join(f"{t} {c:.2f}"
                                   for t, c in perto))
# os erros de digitação do capítulo 19: a palavra certa
# aparece entre os vizinhos?
conta = Counter(t for x in treino for t in palavras(x))


def trocas(t):
    return {t[:j] + t[j + 1] + t[j] + t[j + 2:]
            for j in range(len(t) - 1)}


erros = [t for t in voc.tokens[2:]
         if any(conta.get(s, 0) > conta[t] for s in trocas(t))]
primeiro = cinco = 0
for t in erros:
    certa = max(trocas(t), key=lambda s: conta.get(s, 0))
    perto = [w for w, _ in vizinhos(vetores, voc, t)]
    primeiro += perto[0] == certa
    cinco += certa in perto
print(f"{len(erros)} erros de digitação; a palavra certa")
print(f"  é a mais próxima em {primeiro}")
print(f"  está entre as 5 mais próximas em {cinco}")
# a matriz de cossenos de algumas palavras
GRUPOS = ["agua", "auga", "agau", "casa", "caas", "csaa",
          "tres", "duas", "quatro", "barragem", "rompeu",
          "socorro", "scoorro", "telhado"]
u = vetores / np.linalg.norm(vetores, axis=1, keepdims=True)
ids = [voc.numero[p] for p in GRUPOS]
cos = u[ids] @ u[ids].T
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(cos, cmap="Blues", vmin=0, vmax=1)
ax.set_xticks(range(len(GRUPOS)), GRUPOS, rotation=90)
ax.set_yticks(range(len(GRUPOS)), GRUPOS)
fig.colorbar(im, ax=ax, shrink=0.8)
fig.tight_layout()
fig.savefig("cossenos.png", dpi=300)
