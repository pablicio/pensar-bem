import numpy as np

from rio.numpy_rnn import rnn, rnn_inicia
from rio.serie import ler

chuva = ler("telemetria")["apiuna"]
noite = chuva.loc["2026-10-14 15:00":"2026-10-14 22:00"]
p = rnn_inicia(entradas=1, estado=4,
               sorteio=np.random.default_rng(5))
estados = rnn(p, noite.to_numpy()[:, None] / 10)
np.set_printoptions(precision=2, suppress=True, sign=" ")
for hora, mm, h in zip(noite.index, noite, estados):
    print(f"{hora:%Hh}  {mm:5.1f} mm  {h}")
