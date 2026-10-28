from catalogo import ler_catalogo

titulos, vetores = ler_catalogo("catalogo.csv")
nomes = ["ano", "andamento", "energia", "acustico", "danca",
         "preco"]
raro = vetores[12]
moeda = vetores[0]
for nome, a, b in zip(nomes, raro, moeda):
    print(f"{nome:10s} {a:7.1f} {b:7.1f}"
          f"  diferença² {(a - b) ** 2:10.2f}")
