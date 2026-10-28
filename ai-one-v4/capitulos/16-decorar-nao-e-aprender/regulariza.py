import numpy as np

from numpy_mlp.aumento import desloca
from numpy_mlp.camadas import Rede
from numpy_mlp.dados import mnist_vetores
from numpy_mlp.otimizadores import Adam
from numpy_mlp.treino import avaliar, uma_epoca

(X, y), (Xv, yv), _ = mnist_vetores()
X, y = X[:5_000], y[:5_000]                 # só cinco mil
EPOCAS = 40


def treina(decaimento=0.0, dropout=0.0, aumenta=False):
    rede = Rede([784, 300, 300, 10], dropout=dropout)
    otimizador = Adam(rede, decaimento=decaimento)
    sorteio = np.random.default_rng(0)
    deslocar = np.random.default_rng(1)
    aumento = None
    if aumenta:
        def aumento(lote):
            return desloca(lote, deslocar)
    melhor = (np.inf, 0, 0.0)          # perda, época, acerto
    for epoca in range(1, EPOCAS + 1):
        rede.modo(treinando=True)
        uma_epoca(rede, otimizador, X, y, 64, sorteio, aumento)
        rede.modo(treinando=False)
        perda_v, acerto_v = avaliar(rede, Xv, yv)
        melhor = min(melhor, (perda_v, epoca, acerto_v))
    return avaliar(rede, X, y)[1], acerto_v, melhor


tres = {"decaimento": 1e-3, "dropout": 0.5, "aumenta": True}
receitas = {"nada": {},
            "decaimento 1e-3": {"decaimento": 1e-3},
            "dropout 0,5": {"dropout": 0.5},
            "deslocamentos": {"aumenta": True},
            "os três juntos": tres}
print("técnica          treino  validação   parando na melhor")
for nome, kw in receitas.items():
    treino, valid, (_, epoca, acerto) = treina(**kw)
    print(f"{nome:16} {treino:7.2%} {valid:10.2%}"
          f"   época {epoca:2}: {acerto:.2%}")
