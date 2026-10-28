import numpy as np

from numpy_mlp.camadas import Rede
from numpy_mlp.dados import mnist_vetores
from numpy_mlp.otimizadores import SGD
from numpy_mlp.treino import avaliar, uma_epoca

(X, y), (Xv, yv), _ = mnist_vetores()
print("início   validação após as épocas 1, 2 e 3")
for inicio in ["pequena", "xavier", "he"]:
    rede = Rede([784] + [100] * 9 + [10], inicio=inicio)
    otimizador = SGD(rede, 0.01)
    sorteio = np.random.default_rng(0)
    acertos = []
    for epoca in range(3):
        uma_epoca(rede, otimizador, X, y, 64, sorteio)
        acertos.append(avaliar(rede, Xv, yv)[1])
    linha = "  ".join(f"{a:7.2%}" for a in acertos)
    print(f"{inicio:8} {linha}")
