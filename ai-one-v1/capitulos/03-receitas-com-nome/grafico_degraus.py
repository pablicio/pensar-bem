import matplotlib.pyplot as plt

from frete import frete

pesos = list(range(10, 4001, 10))
fretes = []
for p in pesos:
    fretes.append(frete(p))

plt.figure(figsize=(6, 3.5))
plt.step(pesos, fretes, where="post")
plt.xlabel("peso do pacote (g)")
plt.ylabel("frete (R$)")
plt.savefig("frete_degraus.png", dpi=300, bbox_inches="tight")
print(len(pesos), "pesos, de", pesos[0], "a", pesos[-1],
      "gramas")
print("maior frete:", max(fretes))
