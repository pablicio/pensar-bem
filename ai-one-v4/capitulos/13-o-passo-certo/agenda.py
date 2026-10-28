import math

import numpy as np

from numpy_mlp.camadas import Rede
from numpy_mlp.dados import mnist_vetores
from numpy_mlp.otimizadores import Adam
from numpy_mlp.treino import avaliar, uma_epoca

(X, y), (Xv, yv), _ = mnist_vetores()
EPOCAS = 10


def cosseno(epoca, inicial=2e-3):
    """Desce de `inicial` a zero em meia volta de cosseno."""
    volta = math.pi * epoca / EPOCAS
    return inicial * 0.5 * (1 + math.cos(volta))


resultados = {}
for nome in ["constante", "cosseno"]:
    rede = Rede([784, 100, 10], semente=0)
    otimizador = Adam(rede, 1e-3)
    sorteio = np.random.default_rng(0)
    for epoca in range(EPOCAS):
        if nome == "cosseno":
            otimizador.taxa = cosseno(epoca)
        uma_epoca(rede, otimizador, X, y, 64, sorteio)
    resultados[nome] = avaliar(rede, Xv, yv)

for epoca in (0, 3, 6, 9):
    taxa = cosseno(epoca)
    print(f"cosseno, época {epoca + 1:2}: taxa {taxa:.1e}")
for nome, (perda, acerto) in resultados.items():
    print(f"{nome:9}: perda valid. {perda:.4f},"
          f" acerto {acerto:.2%}")
