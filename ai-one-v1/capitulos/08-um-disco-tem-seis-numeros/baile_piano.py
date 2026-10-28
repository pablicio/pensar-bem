from catalogo import ler_catalogo
from operacoes import escalar, soma

titulos, vetores = ler_catalogo("catalogo.csv")
total = soma(vetores[8], vetores[11])
print(total)
print(escalar(0.5, total))
