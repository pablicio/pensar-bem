import time

import numpy as np

from numpy_mlp.camadas import Rede
from numpy_mlp.dados import mnist_vetores
from numpy_mlp.otimizadores import SGD
from numpy_mlp.treino import avaliar, uma_epoca

(X, y), (Xv, yv), _ = mnist_vetores()
print("  lote  passos  acerto valid. após uma época")
for lote in [8, 64, 512, 50_000]:
    rede = Rede([784, 100, 10], semente=0)
    uma_epoca(rede, SGD(rede, 0.1), X, y, lote,
              np.random.default_rng(0))
    _, av = avaliar(rede, Xv, yv)
    passos = -(-len(X) // lote)            # divisão para cima
    print(f"{lote:6,} {passos:7,} {av:14.2%}")
