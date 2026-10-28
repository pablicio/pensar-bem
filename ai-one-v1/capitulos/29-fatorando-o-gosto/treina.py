import matplotlib.pyplot as plt

from fatoracao import matriz, recomendar_fatores, treinar
from loja import gerar_loja

discos, compras = gerar_loja(2027)
treino = [c[:-1] for c in compras]
r = matriz(treino, len(discos))
p, q, b, historico = treinar(r, k=2, eta=0.004, lam=0.1,
                             epocas=300, semente=2)
print(f"perda: época 1 {historico[0]:.1f}, "
      f"época 300 {historico[-1]:.1f}")
acertos = 0
for c, todas in enumerate(compras):
    if todas[-1] in recomendar_fatores(c, treino[c], p, q, b):
        acertos += 1
print(f"taxa de acerto em 10: {acertos / len(compras):.3f}")

plt.figure(figsize=(6, 3.5))
plt.plot(range(1, 301), historico)
plt.xlabel("época")
plt.ylabel("perda")
plt.savefig("perda_fatoracao.png", dpi=300,
            bbox_inches="tight")
