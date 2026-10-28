import matplotlib.pyplot as plt
import numpy as np

from numpy_mlp.camadas import Rede, softmax_entropia
from numpy_mlp.dados import mnist_vetores
from numpy_mlp.otimizadores import Adam

(X, y), _, _ = mnist_vetores()
rede = Rede([784, 100, 10], semente=0)
otimizador = Adam(rede)
ordem = np.random.default_rng(0).permutation(len(X))

# 400 passos, com a taxa crescendo de 10⁻⁶ a 1 em escala log
taxas = np.logspace(-6, 0, 400)
perdas = []
for taxa, k in zip(taxas, range(0, 400 * 64, 64)):
    otimizador.taxa = taxa
    i = ordem[k:k + 64]
    perda, dZ = softmax_entropia(rede.frente(X[i]), y[i])
    rede.volta(dZ)
    otimizador.passo()
    perdas.append(perda)

media = np.convolve(perdas, np.ones(21) / 21, "valid")
centro = taxas[10:-10]        # a taxa no meio de cada média
fundo = media.argmin()
queda = np.gradient(media, np.log10(centro))[:fundo]
print(f"a perda desce mais depressa perto de"
      f" {centro[queda.argmin()]:.0e}")
print(f"e é mínima perto de {centro[fundo]:.0e};"
      f" depois, sobe")

fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(centro, media)
ax.set_xscale("log")
ax.set_xlabel("taxa de aprendizado")
ax.set_ylabel("perda (média de 20 lotes)")
ax.set_ylim(0, 3)
fig.tight_layout()
fig.savefig("faixa.png", dpi=300)
