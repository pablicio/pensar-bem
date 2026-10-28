import numpy as np

from numpy_mlp.camadas import Rede, softmax_entropia

sorteio = np.random.default_rng(1)
X = sorteio.normal(size=(8, 5))
y = np.array([0, 2, 1, 2, 0, 1, 1, 0])
rede = Rede([5, 4, 3], normaliza=True)
print(" ".join(type(c).__name__ for c in rede.camadas))


def perda():
    return softmax_entropia(rede.frente(X), y)[0]


rede.volta(softmax_entropia(rede.frente(X), y)[1])
eps, pior, total = 1e-6, 0.0, 0
for camada, valor, nome in rede.parametros():
    grad = getattr(camada, nome)
    for i in np.ndindex(valor.shape):
        guarda = valor[i]
        valor[i] = guarda + eps
        mais = perda()
        valor[i] = guarda - eps
        menos = perda()
        valor[i] = guarda
        num = (mais - menos) / (2 * eps)
        maior = max(abs(grad[i]), abs(num), 1e-8)
        pior = max(pior, abs(grad[i] - num) / maior)
        total += 1
print(f"{total} parâmetros; maior diferença relativa:"
      f" {pior:.1e}")
