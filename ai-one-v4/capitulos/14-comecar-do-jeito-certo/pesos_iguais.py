import numpy as np

from numpy_mlp.camadas import Rede
from numpy_mlp.dados import mnist_vetores
from numpy_mlp.otimizadores import Adam
from numpy_mlp.treino import avaliar, uma_epoca

(X, y), (Xv, yv), _ = mnist_vetores()
rede = Rede([784, 100, 10], semente=0)
for c in rede.camadas[::2]:            # as camadas lineares
    c.W[:] = 0.01                      # todos os pesos iguais

uma_epoca(rede, Adam(rede), X, y, 64, np.random.default_rng(0))
W1 = rede.camadas[0].W
iguais = np.unique(W1.round(10), axis=1).shape[1]
print(f"neurônios escondidos diferentes entre si: {iguais}")
print(f"acerto na validação: {avaliar(rede, Xv, yv)[1]:.2%}")
