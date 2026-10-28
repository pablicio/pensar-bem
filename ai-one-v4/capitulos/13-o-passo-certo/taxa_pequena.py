import numpy as np

from numpy_mlp.camadas import Rede
from numpy_mlp.dados import mnist_vetores
from numpy_mlp.otimizadores import Adam
from numpy_mlp.treino import avaliar, uma_epoca

(X, y), (Xv, yv), _ = mnist_vetores()
for taxa in [1e-5, 1e-3]:
    rede = Rede([784, 100, 10], semente=0)
    uma_epoca(rede, Adam(rede, taxa), X, y, 64,
              np.random.default_rng(0))
    perda, acerto = avaliar(rede, Xv, yv)
    print(f"taxa {taxa:.0e}: perda {perda:.3f},"
          f" acerto {acerto:.2%}")
