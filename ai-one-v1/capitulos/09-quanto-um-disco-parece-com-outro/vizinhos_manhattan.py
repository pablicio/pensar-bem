from catalogo import ler_catalogo
from distancias import manhattan
from normaliza import normalizar

titulos, vetores = ler_catalogo("catalogo.csv")
normais, minimos, maximos = normalizar(vetores)
pares = []
for i in range(12):
    d = manhattan(normais[12], normais[i])
    pares.append((d, titulos[i]))
for d, titulo in sorted(pares)[:3]:
    print(f"  {d:6.3f}  {titulo}")
