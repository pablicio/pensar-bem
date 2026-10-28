from catalogo import ler_catalogo
from distancias import distancia

titulos, vetores = ler_catalogo("catalogo.csv")
alvo = 12            # o frevo raro, último da lista

pares = []
for i in range(len(vetores)):
    if i != alvo:
        d = distancia(vetores[alvo], vetores[i])
        pares.append((d, titulos[i]))
pares = sorted(pares)

print("parecidos com", titulos[alvo])
for d, titulo in pares[:3]:
    print(f"  {d:7.1f}  {titulo}")
