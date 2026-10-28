import numpy as np

sorteio = np.random.default_rng(0)
# três camadas lineares: 2 -> 4 -> 4 -> 1
W1, b1 = sorteio.normal(size=(4, 2)), sorteio.normal(size=4)
W2, b2 = sorteio.normal(size=(4, 4)), sorteio.normal(size=4)
W3, b3 = sorteio.normal(size=(1, 4)), sorteio.normal(size=1)


def tres_camadas(x):
    return W3 @ (W2 @ (W1 @ x + b1) + b2) + b3


# a mesma conta, numa camada só
W = W3 @ W2 @ W1
b = W3 @ (W2 @ b1 + b2) + b3
print("a camada única: W =", W.round(3), " b =", b.round(3))

pontos = sorteio.normal(size=(1000, 2))
dif = max(abs(tres_camadas(x) - (W @ x + b)).max()
          for x in pontos)
print(f"maior diferença em mil pontos: {dif:.1e}")
