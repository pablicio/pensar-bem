import numpy as np

from numpy_mlp.camadas import Rede, softmax_entropia
from numpy_mlp.dados import mnist_vetores
from numpy_mlp.otimizadores import Adam
from numpy_mlp.treino import avaliar

(X, y), (Xv, yv), _ = mnist_vetores()
rede = Rede([784, 100, 10], semente=0)
otimizador = Adam(rede, taxa=1.0)            # a taxa copiada
ordem = np.random.default_rng(0).permutation(len(X))
for passo, k in enumerate(range(0, len(X), 64), start=1):
    i = ordem[k:k + 64]
    perda, dZ = softmax_entropia(rede.frente(X[i]), y[i])
    rede.volta(dZ)
    otimizador.passo()
    if passo in (1, 2, 3, 5, 10, 100, 782):
        print(f"passo {passo:3}: perda do lote {perda:9.2f}")

_, acerto = avaliar(rede, Xv, yv)
primeira = rede.camadas[0]
escondida = np.maximum(0, Xv @ primeira.W + primeira.b)
mortos = (escondida.max(axis=0) == 0).sum()
print(f"\nacerto na validação: {acerto:.2%}")
print(f"neurônios escondidos que nunca ligam: {mortos} de 100")
