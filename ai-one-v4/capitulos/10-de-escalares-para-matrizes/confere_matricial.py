import numpy as np

from numpy_mlp.camadas import Rede, softmax_entropia

sorteio = np.random.default_rng(1)
X = sorteio.normal(size=(6, 5))      # um lote de 6 exemplos
y = np.array([0, 2, 1, 2, 0, 1])
rede = Rede([5, 4, 3])
print(" ".join(type(c).__name__ for c in rede.camadas))


def perda():
    return softmax_entropia(rede.frente(X), y)[0]


p, dZ = softmax_entropia(rede.frente(X), y)
rede.volta(dZ)
print(f"perda do lote: {p:.6f}")

eps, pior, total = 1e-6, 0.0, 0
for camada, valor, nome in rede.parametros():
    grad = getattr(camada, nome)
    print(f"{nome}: {grad.shape}, o formato de {valor.shape}")
    for i in np.ndindex(valor.shape):
        guarda = valor[i]
        valor[i] = guarda + eps
        mais = perda()
        valor[i] = guarda - eps
        menos = perda()
        valor[i] = guarda
        num = (mais - menos) / (2 * eps)
        maior = max(abs(grad[i]), abs(num), 1e-12)
        pior = max(pior, abs(grad[i] - num) / maior)
        total += 1
print(f"{total} parâmetros; maior diferença relativa:"
      f" {pior:.1e}")
