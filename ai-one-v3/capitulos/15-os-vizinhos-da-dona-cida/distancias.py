import numpy as np

sorteio = np.random.default_rng(1)
print("colunas  mais perto / mais longe")
for colunas in [2, 10, 100, 1000]:
    pontos = sorteio.normal(size=(1000, colunas))
    d = np.sqrt(((pontos[1:] - pontos[0]) ** 2).sum(axis=1))
    print(f"{colunas:7} {d.min() / d.max():24.2f}")
