import time

import numpy as np

from mnist import carregar
from motor.rede import Rede as RedeEscalar
from numpy_mlp.camadas import Rede, softmax_entropia

imagens, rotulos = carregar("treino")
X = imagens.reshape(-1, 784) / 255

# o motor escalar: dez dígitos, uma rede 784-30-10
rede = RedeEscalar([784, 30, 10])
inicio = time.perf_counter()
for x, y in zip(X[:10], rotulos[:10]):
    saidas = rede(list(x))
    # o motor não tem a entropia cruzada; a soma basta aqui
    perda = sum(saidas) * 1.0
    perda.backward()
por_digito = (time.perf_counter() - inicio) / 10
print(f"motor escalar: {por_digito * 1000:.0f} ms por dígito;"
      f" uma época: {por_digito * 60_000 / 3600:.1f} h")

# a versão matricial: a época inteira, em lotes de 64
rede = Rede([784, 30, 10])
inicio = time.perf_counter()
for k in range(0, 60_000, 64):
    _, dZ = softmax_entropia(rede.frente(X[k:k + 64]),
                             rotulos[k:k + 64])
    rede.volta(dZ)
segundos = time.perf_counter() - inicio
print(f"NumPy em lotes: uma época em {segundos:.1f} s")
razao = por_digito * 60_000 / segundos
print(f"razão: umas {razao:,.0f} vezes")
