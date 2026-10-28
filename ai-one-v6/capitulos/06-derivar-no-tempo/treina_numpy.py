import numpy as np

from rio.avalia import mae, parte
from rio.janelas import janelas
from rio.numpy_rnn import (rnn_gradiente, rnn_inicia,
                           rnn_previsao)
from rio.serie import nivel_cidade

nivel = nivel_cidade()
x, y, _ = janelas(parte(nivel, "treino"), 24, 6, passo=12)
xv, yv, _ = janelas(parte(nivel, "validacao"), 24, 6, passo=6)
x, y, xv = 10 * x, 10 * y, 10 * xv      # em decímetros
sorteio = np.random.default_rng(0)
p = rnn_inicia(entradas=1, estado=8, sorteio=sorteio)
p["wy"], p["c"] = np.zeros(8), np.array(0.0)
print(len(x), "janelas de treino;"
      f" persistência na validação: {mae(yv) * 100:.2f} cm")
for epoca in range(5):
    perdas, normas = [], []
    for i in sorteio.permutation(len(x)):
        perda, g = rnn_gradiente(p, x[i][:, None], y[i])
        for nome in p:              # a descida do gradiente
            p[nome] = p[nome] - 0.003 * g[nome]
        perdas.append(perda)
        normas.append(np.sqrt(sum((v ** 2).sum()
                                  for v in g.values())))
    prev = np.array([rnn_previsao(p, j[:, None])[0]
                     for j in xv])
    print(f"época {epoca + 1}: perda {np.mean(perdas):.3f},"
          f" validação {mae(prev / 10 - yv) * 100:.2f} cm,"
          f" maior gradiente {max(normas):.0f}")
