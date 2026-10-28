import random

random.seed(3)
p = 116 / 2840
grupos = 200_000
pelo_menos_uma = 0
tres = 0
for _ in range(grupos):
    compraram = 0
    for pessoa in range(3):
        chance = 0.30 if compraram > 0 else p
        if random.random() < chance:
            compraram += 1
    if compraram >= 1:
        pelo_menos_uma += 1
    if compraram == 3:
        tres += 1
print(f"pelo menos uma: {pelo_menos_uma / grupos:.4f}")
print(f"as três:        {tres / grupos:.5f}")
