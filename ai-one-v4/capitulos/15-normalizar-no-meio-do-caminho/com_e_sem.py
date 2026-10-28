import numpy as np

from numpy_mlp.camadas import Rede
from numpy_mlp.dados import mnist_vetores
from numpy_mlp.otimizadores import SGD
from numpy_mlp.treino import avaliar, uma_epoca

(X, y), (Xv, yv), _ = mnist_vetores()
print("rede                  taxa  validação, épocas 1 a 3")
for normaliza in (False, True):
    for taxa in (0.01, 0.1):
        rede = Rede([784] + [100] * 9 + [10],
                    normaliza=normaliza)
        otimizador = SGD(rede, taxa)
        sorteio = np.random.default_rng(0)
        acertos = []
        for epoca in range(3):
            rede.modo(treinando=True)
            uma_epoca(rede, otimizador, X, y, 64, sorteio)
            rede.modo(treinando=False)
            acertos.append(avaliar(rede, Xv, yv)[1])
        nome = "com" if normaliza else "sem"
        linha = "  ".join(f"{a:7.2%}" for a in acertos)
        print(f"{nome} normalização     {taxa:5} {linha}")
