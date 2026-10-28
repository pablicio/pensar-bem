import random

import matplotlib.pyplot as plt

from distribuicoes import poisson

random.seed(2403)
visitas_por_hora = 1140       # sexta, das 19h às 23h
p = 0.007                     # a conversão do site

pedidos_por_hora = []
for _ in range(2000):
    pedidos = 0
    for _ in range(visitas_por_hora):
        if random.random() < p:
            pedidos += 1
    pedidos_por_hora.append(pedidos)

lam = visitas_por_hora * p
acima = sum(1 for x in pedidos_por_hora if x > 12) / 2000
formula = 1 - sum(poisson(k, lam) for k in range(13))
media_hora = sum(pedidos_por_hora) / 2000
print(f"média de pedidos por hora: {media_hora:.2f}")
print(f"mais de 12 numa hora: simulação {acima:.4f},"
      f" Poisson {formula:.4f}")

ks = list(range(0, 21))
plt.figure(figsize=(6, 3.5))
plt.hist(pedidos_por_hora, bins=[k - 0.5 for k in range(22)],
         density=True, color="0.85", edgecolor="0.4")
plt.plot(ks, [poisson(k, lam) for k in ks], marker="o")
plt.xlabel("pedidos numa hora de pico")
plt.ylabel("proporção das horas")
plt.savefig("sextas.png", dpi=300, bbox_inches="tight")
