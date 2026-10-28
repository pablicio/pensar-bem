import matplotlib.pyplot as plt

from fatoracao import matriz, treinar
from loja import gerar_loja, genero

GENEROS = ["frevo", "funk", "viola", "jazz"]
discos, compras = gerar_loja(2027)
r = matriz([c[:-1] for c in compras], len(discos))
p, q, b, _ = treinar(r, k=2, eta=0.004, lam=0.1,
                     epocas=300, semente=2)

print(" " * 19, "frevo  funk viola  jazz")
for f in [0, 1]:
    valores = sorted((q[d][f], d) for d in range(120))
    ordem = [d for _, d in valores]
    pontas = [("início", ordem[:15]), ("fim", ordem[-15:])]
    for nome, ponta in pontas:
        nomes = [genero(discos[d]) for d in ponta]
        n = [nomes.count(g) for g in GENEROS]
        print(f"dimensão {f + 1}, {nome:6} "
              f"{n[0]:5} {n[1]:5} {n[2]:5} {n[3]:5}")

plt.figure(figsize=(5, 5))
for g, marca in zip(GENEROS, ["o", "s", "^", "x"]):
    pontos = [q[d] for d in range(120)
              if genero(discos[d]) == g]
    plt.scatter([x for x, _ in pontos], [y for _, y in pontos],
                marker=marca, color="black", label=g)
plt.xlabel("dimensão 1")
plt.ylabel("dimensão 2")
plt.legend()
plt.savefig("mapa_gosto.png", dpi=300, bbox_inches="tight")
