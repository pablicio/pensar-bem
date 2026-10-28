import matplotlib.pyplot as plt

from duas_alavancas import gradiente, lucro


def perda(preco, centenas):
    # o contrário do lucro, em centenas de R$: menor é melhor
    return -lucro(preco, 100 * centenas) / 100


eta = 1.0
p, c = 89.90, 0.0  # o preço de hoje, sem anúncio
caminho = [(p, c)]
for passo in range(1, 101):
    gp, gc = gradiente(perda, p, c)
    p, c = p - eta * gp, c - eta * gc
    caminho.append((p, c))
    if passo in [1, 2, 5, 20, 100]:
        anuncio, lucro_agora = 100 * c, -100 * perda(p, c)
        print(f"passo {passo:3d}: R$ {p:6.2f},"
              f" anúncio R$ {anuncio:6.1f},"
              f" lucro R$ {lucro_agora:8.2f}")

precos = [80 + 0.25 * i for i in range(61)]
centenas = [0.25 * j for j in range(41)]
Z = [[perda(x, y) for x in precos] for y in centenas]
plt.figure(figsize=(7, 4.2))
plt.contour(precos, centenas, Z, levels=15, colors="0.6",
            linestyles="solid")
plt.plot([q[0] for q in caminho], [q[1] for q in caminho],
         marker="o", markersize=2)
plt.gca().set_aspect("equal")
plt.xlabel("preço da reedição (R$)")
plt.ylabel("anúncio (centenas de R$)")
plt.savefig("descida_loja.png", dpi=300, bbox_inches="tight")
