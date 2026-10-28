import matplotlib.pyplot as plt
import numpy as np

from numpy_mlp.camadas import Rede
from numpy_mlp.dados import mnist_vetores
from numpy_mlp.otimizadores import SGD
from numpy_mlp.treino import avaliar, uma_epoca

(X, y), (Xv, yv), (Xt, yt) = mnist_vetores()
rede = Rede([784, 100, 10], semente=0)
otimizador = SGD(rede, taxa=0.1)
sorteio = np.random.default_rng(0)          # a ordem dos lotes

curva = []
print("época  perda treino  perda valid.  acerto valid.")
for epoca in range(1, 11):
    perdas = uma_epoca(rede, otimizador, X, y, 64, sorteio)
    curva += perdas
    pv, av = avaliar(rede, Xv, yv)
    print(f"{epoca:5} {np.mean(perdas):13.4f} {pv:13.4f}"
          f" {av:14.2%}")

_, at = avaliar(rede, Xt, yt)
print(f"\nno teste, uma vez só: {at:.2%}")

fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(curva, lw=0.3)
ax.set_xlabel("passo (um lote de 64)")
ax.set_ylabel("perda do lote")
ax.set_yscale("log")
fig.tight_layout()
fig.savefig("curva_perda.png", dpi=300)
