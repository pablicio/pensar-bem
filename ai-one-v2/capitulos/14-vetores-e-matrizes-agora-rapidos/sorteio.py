import numpy as np

for vez in range(2):
    gerador = np.random.default_rng(2027_04)
    escolhidos = gerador.choice(140, size=10, replace=False)
    print(np.sort(escolhidos))
