import math

import matplotlib.pyplot as plt

from duas_alavancas import gradiente, lucro


def lucro_c(preco, centenas):
    # o mesmo lucro, com o anúncio medido em centenas de reais
    return lucro(preco, 100 * centenas)


precos = [70 + 0.5 * i for i in range(81)]  # R$ 70 a R$ 110
centenas = [0.25 * j for j in range(81)]    # R$ 0 a R$ 2.000
Z = [[lucro_c(p, c) for p in precos] for c in centenas]

plt.figure(figsize=(7, 4))
linhas = plt.contour(precos, centenas, Z, levels=12,
                     colors="0.4")
plt.clabel(linhas, fontsize=7, fmt="%.0f")

xs, ys, us, vs = [], [], [], []
for p in range(72, 110, 6):
    for c in range(1, 20, 3):
        gx, gy = gradiente(lucro_c, p, c)
        tamanho = math.sqrt(gx ** 2 + gy ** 2)
        xs.append(p)
        ys.append(c)
        us.append(gx / tamanho)
        vs.append(gy / tamanho)
plt.quiver(xs, ys, us, vs, angles="xy", scale_units="xy",
           scale=0.6, width=0.004)
plt.scatter([88], [7.457], marker="*", s=150)
plt.gca().set_aspect("equal")
plt.xlabel("preço da reedição (R$)")
plt.ylabel("anúncio (centenas de R$ por mês)")
plt.savefig("mapa_lucro.png", dpi=300, bbox_inches="tight")
print("lucro no topo:", round(lucro(88, 745.7), 2))
