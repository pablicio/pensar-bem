from catalogo import ler_catalogo
from distancias import distancia
from normaliza import normalizar

titulos, vetores = ler_catalogo("catalogo.csv")
normais, minimos, maximos = normalizar(vetores)
alvo = 12

pares = []
for i in range(len(normais)):
    if i != alvo:
        d = distancia(normais[alvo], normais[i])
        pares.append((d, titulos[i]))
pares = sorted(pares)

print("parecidos com", titulos[alvo], "(normalizado)")
for d, titulo in pares[:3]:
    print(f"  {d:6.3f}  {titulo}")
print("preço normalizado do Frevo na Moeda:",
      round(normais[0][5], 3))
print("preço normalizado do Jazz de Câmara:",
      round(normais[6][5], 3))
