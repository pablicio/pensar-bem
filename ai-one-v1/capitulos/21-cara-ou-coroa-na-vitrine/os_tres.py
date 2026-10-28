import random

random.seed(1)
p = 116 / 2840
print(f"pela conta: {p ** 3:.6f}")
grupos = 100_000
todos = 0
for _ in range(grupos):
    a = random.random() < p
    b = random.random() < p
    c = random.random() < p
    if a and b and c:
        todos += 1
print(f"simulando:  {todos / grupos:.6f}")
