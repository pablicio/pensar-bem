import numpy as np

from rio.numpy_gru import gru_gradiente, gru_inicia

sorteio = np.random.default_rng(4)
p = gru_inicia(entradas=2, estado=3, sorteio=sorteio)
p["bzr"] += sorteio.normal(0, 0.3, 6)
p["wy"], p["c"] = sorteio.normal(0, 1, 3), np.array(0.1)
xs = sorteio.normal(0, 1, (5, 2))
_, g = gru_gradiente(p, xs, 0.7)
eps = 1e-6
for nome, peso in p.items():
    numerico = np.zeros_like(peso)
    for i in np.ndindex(peso.shape):
        guarda = peso[i]
        peso[i] = guarda + eps
        mais, _ = gru_gradiente(p, xs, 0.7)
        peso[i] = guarda - eps
        menos, _ = gru_gradiente(p, xs, 0.7)
        peso[i] = guarda
        numerico[i] = (mais - menos) / (2 * eps)
    dif = np.abs(numerico - g[nome]).max()
    print(f"{nome:3} {str(peso.shape):8}"
          f" {dif / np.abs(numerico).max():.1e}")
