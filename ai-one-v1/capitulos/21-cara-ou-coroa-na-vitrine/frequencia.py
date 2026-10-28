import random

import matplotlib.pyplot as plt

random.seed(2027)
p = 116 / 2840

compras = 0
frequencias = []
for i in range(1, 10_001):
    if random.random() < p:
        compras += 1
    frequencias.append(compras / i)

plt.figure(figsize=(6, 3.5))
plt.plot(range(1, 10_001), frequencias)
plt.axhline(p, linestyle="--", color="0.4")
plt.xscale("log")
plt.xlabel("visitantes (escala log)")
plt.ylabel("fração que comprou")
plt.savefig("frequencia.png", dpi=300, bbox_inches="tight")
print(f"depois de 10: {frequencias[9]:.3f};"
      f" de 10.000: {frequencias[-1]:.4f}")
