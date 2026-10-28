import matplotlib.pyplot as plt

from catalogo import ler_catalogo
from operacoes import media

titulos, vetores = ler_catalogo("catalogo.csv")
# só energia (posição 2) e acústico (3) de cada disco
frevo = [vetores[0][2], vetores[0][3]]
choro = [vetores[3][2], vetores[3][3]]
meio = media([frevo, choro])
print("frevo", frevo, "choro", choro, "média", meio)

plt.figure(figsize=(5, 5))
for v, estilo, nome in [(frevo, "-", "frevo"),
                        (choro, "--", "choro"),
                        (meio, ":", "média")]:
    plt.annotate("", xy=v, xytext=(0, 0),
                 arrowprops={"arrowstyle": "->",
                             "linestyle": estilo})
    plt.text(v[0] + 0.02, v[1] + 0.02, nome)
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel("energia")
plt.ylabel("acústico")
plt.savefig("setas.png", dpi=300, bbox_inches="tight")
