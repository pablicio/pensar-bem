import numpy as np

from rio.numpy_rnn import rnn_gradiente, rnn_inicia

sorteio = np.random.default_rng(6)
p = rnn_inicia(entradas=2, estado=3, sorteio=sorteio)
p["b"] = sorteio.normal(0, 0.3, 3)
p["wy"] = sorteio.normal(0, 1, 3)
p["c"] = np.array(0.1)
xs = sorteio.normal(0, 1, (5, 2))   # 5 passos, 2 entradas
alvo = 0.7

perda, g = rnn_gradiente(p, xs, alvo)
eps = 1e-6
print("peso  forma   maior diferença relativa")
for nome, peso in p.items():
    numerico = np.zeros_like(peso)
    for i in np.ndindex(peso.shape):
        guarda = peso[i]
        peso[i] = guarda + eps
        mais, _ = rnn_gradiente(p, xs, alvo)
        peso[i] = guarda - eps
        menos, _ = rnn_gradiente(p, xs, alvo)
        peso[i] = guarda
        numerico[i] = (mais - menos) / (2 * eps)
    dif = (np.abs(numerico - g[nome]).max()
           / np.abs(numerico).max())
    print(f"{nome:4}  {str(peso.shape):7} {dif:.1e}")
