import math

from catalogo import ler_catalogo
from normaliza import normalizar


def distancia_ponderada(u, v, pesos):
    total = 0
    for a, b, w in zip(u, v, pesos):
        total += w * (a - b) ** 2
    return math.sqrt(total)


titulos, vetores = ler_catalogo("catalogo.csv")
normais, minimos, maximos = normalizar(vetores)
pesos = [1, 1, 3, 3, 3, 1]
pares = []
for i in range(12):
    d = distancia_ponderada(normais[12], normais[i], pesos)
    pares.append((d, titulos[i]))
for d, titulo in sorted(pares)[:3]:
    print(f"  {d:6.3f}  {titulo}")
