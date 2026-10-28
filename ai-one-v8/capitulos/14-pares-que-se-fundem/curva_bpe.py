import time

import matplotlib.pyplot as plt

from lupa.bpe import BPE
from lupa.diario import atos

corpus = atos()
treino = "\n".join(a["texto"] for a in corpus[:300])
novos = [a for a in corpus if a["data"] >= "2027"]
teste = [a["texto"] for a in novos[:200]]
n_bytes = sum(len(t.encode("utf-8")) for t in teste)

inicio = time.time()
completo = BPE()
completo.treina(treino, 2000)
print(f"treino até V = 2000: {time.time() - inicio:.0f} s")

tamanhos = [256, 300, 400, 500, 750, 1000, 1500, 2000]
taxas = []
for V in tamanhos:
    bpe = BPE()
    fusoes, vocab = completo.fusoes, completo.vocab
    bpe.fusoes = {p: n for p, n in fusoes.items() if n < V}
    bpe.vocab = {i: b for i, b in vocab.items() if i < V}
    n = sum(len(bpe.codifica(t)) for t in teste)
    taxas.append(n_bytes / n)
    print(f"V = {V:5}  {n_bytes / n:.2f} bytes por token")

fig, eixo = plt.subplots(figsize=(6, 3))
eixo.plot(tamanhos, taxas, "o-")
eixo.set_xlabel("tamanho do vocabulário V")
eixo.set_ylabel("bytes por token")
fig.tight_layout()
fig.savefig("curva_bpe.png", dpi=300)
