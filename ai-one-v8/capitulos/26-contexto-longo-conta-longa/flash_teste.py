import time
import tracemalloc

import numpy as np

from lupa.atencao_numpy import atencao, softmax
from lupa.flash import atencao_em_blocos, softmax_online

rng = np.random.default_rng(0)
z = rng.normal(size=1000) * 30
dif = np.abs(softmax_online(z, 64) - softmax(z)).max()
print(f"softmax online - softmax: {dif:.1e}")


def mede(f, *args):
    """O resultado, o pico de memória (MB) e o tempo (s)."""
    tracemalloc.start()
    inicio = time.time()
    r = f(*args)
    tempo = time.time() - inicio
    pico = tracemalloc.get_traced_memory()[1] / 1e6
    tracemalloc.stop()
    return r, pico, tempo


d = 64
print("    T  diferença  pico MB  em blocos  tempo s  blocos")
for T in [512, 2048, 8192]:
    Q, K, V = (rng.normal(size=(T, d)) for _ in range(3))
    (padrao, _), mb, s = mede(atencao, Q, K, V)
    blocos, mb_b, s_b = mede(atencao_em_blocos, Q, K, V)
    dif = np.abs(padrao - blocos).max()
    print(f"{T:5}  {dif:9.1e}  {mb:7.1f}  {mb_b:9.1f}"
          f"  {s:7.2f}  {s_b:6.2f}")
