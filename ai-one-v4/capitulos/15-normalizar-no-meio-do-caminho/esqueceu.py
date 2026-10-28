import numpy as np

from numpy_mlp.camadas import Rede
from numpy_mlp.dados import mnist_vetores
from numpy_mlp.otimizadores import SGD
from numpy_mlp.treino import avaliar, uma_epoca

(X, y), (Xv, yv), _ = mnist_vetores()
rede = Rede([784] + [100] * 9 + [10], normaliza=True)
otimizador, sorteio = SGD(rede, 0.1), np.random.default_rng(0)
for epoca in range(3):
    uma_epoca(rede, otimizador, X, y, 64, sorteio)

# a mesma rede, lendo os dígitos de jeitos diferentes
casos = [("avaliação, lotes de 1.000", False, 1_000),
         ("avaliação, um dígito por vez", False, 1),
         ("treino, lotes de 1.000", True, 1_000),
         ("treino, lotes de 8", True, 8),
         ("treino, um dígito por vez", True, 1)]
for nome, treinando, lote in casos:
    rede.modo(treinando)
    _, acerto = avaliar(rede, Xv[:2_000], yv[:2_000], lote)
    print(f"{nome:29} {acerto:7.2%}")
