from catalogo import ler_catalogo
from operacoes import media

titulos, vetores = ler_catalogo("catalogo.csv")
sabado = [vetores[0], vetores[1], vetores[9]]  # 1, 2 e 10
perfil = media(sabado)
for nome, valor in zip(["ano", "andamento", "energia",
                        "acustico", "danca", "preco"], perfil):
    print(f"{nome:10s} {valor:8.2f}")
