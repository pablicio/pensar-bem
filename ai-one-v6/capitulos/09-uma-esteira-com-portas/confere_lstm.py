import numpy as np

from rio.numpy_lstm import lstm_gradiente, lstm_inicia

sorteio = np.random.default_rng(3)
p = lstm_inicia(entradas=2, estado=3, sorteio=sorteio)
p["b"] += sorteio.normal(0, 0.3, 12)
p["wy"], p["c"] = sorteio.normal(0, 1, 3), np.array(0.1)
xs = sorteio.normal(0, 1, (5, 2))
_, g = lstm_gradiente(p, xs, 0.7)
eps = 1e-6
for nome, peso in p.items():
    numerico = np.zeros_like(peso)
    for i in np.ndindex(peso.shape):
        guarda = peso[i]
        peso[i] = guarda + eps
        mais, _ = lstm_gradiente(p, xs, 0.7)
        peso[i] = guarda - eps
        menos, _ = lstm_gradiente(p, xs, 0.7)
        peso[i] = guarda
        numerico[i] = (mais - menos) / (2 * eps)
    dif = np.abs(numerico - g[nome]).max()
    print(f"{nome:2} {str(peso.shape):8}"
          f" {dif / np.abs(numerico).max():.1e}")
