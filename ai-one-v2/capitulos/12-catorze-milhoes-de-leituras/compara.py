import math
import time

import numpy as np

energia = np.load("dados/processados/leituras_ano.npy")

# com listas: um número de cada vez
inicio = time.perf_counter()
fabricante_a = energia[:64].ravel().tolist()
outros = energia[64:].ravel().tolist()
total = 0.0
for valor in fabricante_a:
    if not math.isnan(valor):
        total += valor / 1000           # Wh -> kWh
for valor in outros:
    if not math.isnan(valor):
        total += valor
tempo_lista = time.perf_counter() - inicio

# com o array: a conta inteira de uma vez
inicio = time.perf_counter()
total_np = (np.nansum(energia[:64]) / 1000
            + np.nansum(energia[64:]))
tempo_array = time.perf_counter() - inicio

print(f"listas: {total / 1000:,.3f} MWh")
print(f"array:  {total_np / 1000:,.3f} MWh")
print(f"tempo: {tempo_lista:.2f} s contra {tempo_array:.4f} s")
razao = tempo_lista / tempo_array
print(f"o array foi {razao:.0f} vezes mais rápido")
