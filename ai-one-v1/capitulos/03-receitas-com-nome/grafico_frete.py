import matplotlib.pyplot as plt

from frete import frete, peso_pacote

discos = list(range(1, 11))
pesos = []
fretes = []
for n in discos:
    p = peso_pacote(n)
    pesos.append(p)
    fretes.append(frete(p))

plt.figure(figsize=(6, 3.5))
plt.plot(pesos, fretes, marker="o")
plt.xlabel("peso do pacote (g)")
plt.ylabel("frete (R$)")
plt.savefig("frete_pontos.png", dpi=300, bbox_inches="tight")
print(len(pesos), "pontos;", pesos[0], "a", pesos[-1],
      "gramas")
