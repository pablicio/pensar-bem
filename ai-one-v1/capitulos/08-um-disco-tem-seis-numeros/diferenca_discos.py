from catalogo import ler_catalogo
from operacoes import escalar, soma

titulos, vetores = ler_catalogo("catalogo.csv")
dif = soma(vetores[0], escalar(-1, vetores[3]))
for valor in dif:
    print(f"{valor:8.2f}")
