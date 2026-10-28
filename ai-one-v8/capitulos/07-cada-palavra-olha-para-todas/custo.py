import time

import numpy as np

from lupa.atencao_numpy import atencao

rng = np.random.default_rng(0)
d = 64
print("     T    tempo (ms)   memória das notas (MB)")
for T in [512, 1024, 2048, 4096]:
    Q, K, V = (rng.normal(size=(T, d)) for _ in range(3))
    inicio = time.perf_counter()
    for _ in range(3):
        atencao(Q, K, V)
    ms = (time.perf_counter() - inicio) / 3 * 1000
    print(f"{T:6} {ms:12.1f} {T * T * 8 / 2**20:22.1f}")
