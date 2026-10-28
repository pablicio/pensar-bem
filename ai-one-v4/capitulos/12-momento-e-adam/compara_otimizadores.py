import matplotlib.pyplot as plt
import numpy as np

from numpy_mlp.camadas import Rede
from numpy_mlp.dados import mnist_vetores
from numpy_mlp.otimizadores import SGD, Adam, Momento
from numpy_mlp.treino import avaliar, uma_epoca

(X, y), (Xv, yv), _ = mnist_vetores()
receitas = {"SGD, taxa 0,1": lambda r: SGD(r, 0.1),
            "momento, taxa 0,01": lambda r: Momento(r, 0.01),
            "Adam, taxa 0,001": lambda r: Adam(r, 1e-3)}

fig, ax = plt.subplots(figsize=(7, 3.2))
print("otimizador          valid. após 1, 2 e 3 épocas")
for nome, cria in receitas.items():
    rede = Rede([784, 100, 10], semente=0)    # mesmo começo
    otimizador = cria(rede)
    sorteio = np.random.default_rng(0)        # mesmos lotes
    curva, acertos = [], []
    for epoca in range(3):
        curva += uma_epoca(rede, otimizador, X, y, 64, sorteio)
        acertos.append(avaliar(rede, Xv, yv)[1])
    media = np.convolve(curva, np.ones(100) / 100, "valid")
    ax.plot(media, label=nome)
    linha = "  ".join(f"{a:.2%}" for a in acertos)
    print(f"{nome:19} {linha}")
ax.set_xlabel("passo")
ax.set_ylabel("perda (média de 100 lotes)")
ax.set_yscale("log")
ax.legend()
fig.tight_layout()
fig.savefig("otimizadores.png", dpi=300)
