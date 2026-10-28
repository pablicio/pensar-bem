import time

import numpy as np

from rio.numpy_gru import gru_gradiente, gru_inicia
from rio.numpy_gru import gru_previsao
from rio.numpy_lstm import lstm_gradiente, lstm_inicia
from rio.numpy_lstm import lstm_previsao
from rio.numpy_rnn import rnn_gradiente, rnn_inicia
from rio.numpy_rnn import rnn_previsao
from rio.numpy_treino import adam_inicia, epoca, tarefa_soma

sorteio = np.random.default_rng(0)
x, y = tarefa_soma(sorteio, 2000, 50)
xv, yv = tarefa_soma(sorteio, 500, 50)
redes = {"RNN": (rnn_inicia, rnn_gradiente, rnn_previsao),
         "LSTM": (lstm_inicia, lstm_gradiente, lstm_previsao),
         "GRU": (gru_inicia, gru_gradiente, gru_previsao)}
print("rede  parâmetros  s/época  erro final  abaixo de 0,01")
for nome, (inicia, gradiente, previsao) in redes.items():
    s = np.random.default_rng(1)
    p = inicia(2, 16, s)
    p["wy"], p["c"] = np.zeros(16), np.array(1.0)
    n = sum(v.size for v in p.values())
    adam = adam_inicia(p)
    inicio, primeira = time.perf_counter(), "-"
    for e in range(8):
        epoca(p, gradiente, x, y, s, 0.003, 1.0, adam)
        prev = np.array([previsao(p, q)[0] for q in xv])
        erro = np.mean((prev - yv) ** 2)
        if erro < 0.01 and primeira == "-":
            primeira = f"época {e + 1}"
    segundos = (time.perf_counter() - inicio) / 8
    print(f"{nome:5} {n:10d} {segundos:8.1f} {erro:11.4f}"
          f"  {primeira}")
