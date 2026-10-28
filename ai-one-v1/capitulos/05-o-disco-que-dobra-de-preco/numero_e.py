import math

for n in [1, 2, 4, 12, 365, 10000, 1000000]:
    print(f"{n:8d} vezes por ano: {(1 + 1 / n) ** n:.6f}")
print(f"math.e:                 {math.e:.6f}")
