import numpy as np

from rio.numpy_rnn import (rnn_gradiente, rnn_inicia,
                           rnn_previsao)
from rio.numpy_treino import adam_inicia, epoca

sorteio = np.random.default_rng(1990)
a, b = sorteio.integers(0, 2, (2, 1000))
bits = np.stack([a, b, a ^ b], axis=1).ravel().astype(float)
janela = 6
deslizante = np.lib.stride_tricks.sliding_window_view
x = deslizante(bits[:-1], janela)
y = bits[janela:]
posicao = np.arange(janela, len(bits)) % 3   # 2: o bit do XOR
treino, teste = slice(0, 2400), slice(2400, None)
p = rnn_inicia(entradas=1, estado=4, sorteio=sorteio)
p["wy"], p["c"] = np.zeros(4), np.array(0.5)
adam = adam_inicia(p)
for _ in range(10):
    epoca(p, rnn_gradiente, x[treino, :, None], y[treino],
          sorteio, 0.01, 1.0, adam)
prev = np.array([rnn_previsao(p, j[:, None])[0]
                 for j in x[teste]])
erro = (prev - y[teste]) ** 2
for k, nome in enumerate(["primeiro", "segundo", "XOR"]):
    print(f"bit {nome:8}: erro quadrático médio"
          f" {erro[posicao[teste] == k].mean():.3f}")
