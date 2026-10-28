import matplotlib.pyplot as plt

primeira_semana = 80  # cópias na semana do lançamento
meia_vida = 3         # semanas até as vendas caírem à metade

semanas = list(range(0, 52))
vendas = []
for s in semanas:
    vendas.append(primeira_semana * 0.5 ** (s / meia_vida))

for s in [0, 3, 6, 9, 12]:
    print(f"semana {s:2d}: {vendas[s]:5.1f} cópias")
print(f"total em 52 semanas: {sum(vendas):.0f} cópias")

plt.figure(figsize=(6, 3.5))
plt.plot(semanas, vendas, marker="o", markersize=3)
plt.xlabel("semanas desde o lançamento")
plt.ylabel("cópias vendidas na semana")
plt.savefig("reedicao.png", dpi=300, bbox_inches="tight")
