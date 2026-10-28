from catalogo import ler_catalogo

titulos, vetores = ler_catalogo("catalogo.csv")
print(len(titulos), "discos,", len(vetores[0]), "números cada")
for titulo, v in zip(titulos[:6], vetores[:6]):
    print(f"{titulo:25s} {v}")
