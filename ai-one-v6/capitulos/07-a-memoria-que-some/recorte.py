import numpy as np

from rio.avalia import mae, parte
from rio.janelas import janelas
from rio.numpy_rnn import (rnn_gradiente, rnn_inicia,
                           rnn_previsao)
from rio.numpy_treino import epoca
from rio.serie import nivel_cidade

nivel = nivel_cidade()
x, y, _ = janelas(parte(nivel, "treino"), 24, 6, passo=12)
xv, yv, _ = janelas(parte(nivel, "validacao"), 24, 6, passo=6)
x, y, xv = 10 * x[:, :, None], 10 * y, 10 * xv[:, :, None]
sorteio = np.random.default_rng(0)
p = rnn_inicia(entradas=1, estado=8, sorteio=sorteio)
p["wy"], p["c"] = np.zeros(8), np.array(0.0)
for e in range(5):
    epoca(p, rnn_gradiente, x, y, sorteio, 0.003, limite=1.0)
    prev = np.array([rnn_previsao(p, j)[0] for j in xv]) / 10
    erro = mae(prev - yv) * 100
    print(f"época {e + 1}: validação {erro:.2f} cm")
