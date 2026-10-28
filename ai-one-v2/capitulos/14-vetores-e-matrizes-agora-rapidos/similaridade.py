import math
import time

import numpy as np

diario = np.load("dados/processados/diario.npy")
usinas = np.array([diario[:64].sum(axis=0),
                   diario[64:110].sum(axis=0),
                   diario[110:].sum(axis=0)])


def produto(a, b):
    return sum(x * y for x, y in zip(a, b))


def cosseno(a, b):
    normas = math.sqrt(produto(a, a) * produto(b, b))
    return produto(a, b) / normas


# Python puro, como no volume 1
inicio = time.perf_counter()
listas = usinas.tolist()
puro = [[cosseno(a, b) for b in listas] for a in listas]
tempo_puro = time.perf_counter() - inicio

# NumPy: normalizar as linhas e multiplicar pela transposta
inicio = time.perf_counter()
normas = np.linalg.norm(usinas, axis=1, keepdims=True)
unitarias = usinas / normas
sim = unitarias @ unitarias.T
tempo_numpy = time.perf_counter() - inicio

print(sim.round(4))
print("iguais até a 12ª casa:",
      np.allclose(puro, sim, rtol=0, atol=1e-12))
print(f"tempos: {tempo_puro * 1000:.2f} ms e "
      f"{tempo_numpy * 1000:.3f} ms")
