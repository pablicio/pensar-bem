import numpy as np

from rio.numpy_rnn import (rnn_gradiente, rnn_inicia,
                           rnn_previsao)
from rio.numpy_treino import adam_inicia, epoca, tarefa_soma

print("passos  chutar a média  RNN depois de 8 épocas")
for passos in (10, 20, 50):
    sorteio = np.random.default_rng(0)
    x, y = tarefa_soma(sorteio, 2000, passos)
    xv, yv = tarefa_soma(sorteio, 500, passos)
    p = rnn_inicia(entradas=2, estado=16, sorteio=sorteio)
    p["wy"], p["c"] = np.zeros(16), np.array(1.0)
    adam = adam_inicia(p)
    for _ in range(8):
        epoca(p, rnn_gradiente, x, y, sorteio, 0.003, 1.0,
              adam)
    prev = np.array([rnn_previsao(p, s)[0] for s in xv])
    print(f"{passos:5d}   {np.var(yv):14.4f}"
          f"  {np.mean((prev - yv) ** 2):10.4f}")
