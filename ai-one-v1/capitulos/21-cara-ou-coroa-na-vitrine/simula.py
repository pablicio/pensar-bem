import random

random.seed(2027)
p = 116 / 2840  # fração de fevereiro, pelo contador da porta

for n in [10, 100, 1_000, 10_000, 100_000]:
    compras = 0
    for _ in range(n):
        if random.random() < p:
            compras += 1
    print(f"{n:7,d} visitantes: {compras:6,d} compras, "
          f"frequência {compras / n:.4f}")
print(f"probabilidade usada: {p:.4f}")
