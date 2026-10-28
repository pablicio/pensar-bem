from catalogo import ler_catalogo
from operacoes import media

titulos, vetores = ler_catalogo("catalogo.csv")
perfil = media([vetores[3], vetores[5], vetores[6]])
for valor in perfil:
    print(f"{valor:8.2f}")
