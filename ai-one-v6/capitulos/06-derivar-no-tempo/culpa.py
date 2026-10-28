import numpy as np

from rio.numpy_rnn import rnn_gradiente, rnn_inicia
from rio.serie import nivel_cidade

nivel = nivel_cidade()
janela = nivel.loc["2008-11-23 06:00":"2008-11-24 05:00"]
xs = 10 * (janela - janela.iloc[-1]).to_numpy()[:, None]
sorteio = np.random.default_rng(0)
p = rnn_inicia(entradas=1, estado=8, sorteio=sorteio)
p["wy"], p["c"] = sorteio.normal(0, 1, 8), np.array(0.0)
anterior = np.zeros_like(p["Wh"])
print("passo para trás   culpa em W_h")
for k in range(1, 25):
    _, g = rnn_gradiente(p, xs, alvo=1.0, truncar=k)
    if k in (1, 2, 3, 6, 12, 18, 23):
        nova = np.linalg.norm(g["Wh"] - anterior)
        print(f"{k:10d} {nova:18.2e}")
    anterior = g["Wh"].copy()
