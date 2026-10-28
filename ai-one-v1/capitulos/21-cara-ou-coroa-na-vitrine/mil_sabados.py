import random

random.seed(7)
p = 116 / 2840
contagem = [0] * 11
for _ in range(1000):
    compras = 0
    for _ in range(10):
        if random.random() < p:
            compras += 1
    contagem[compras] += 1
print("nenhuma compra:", contagem[0])
print("uma compra:    ", contagem[1])
print("duas ou mais:  ", sum(contagem[2:]))
