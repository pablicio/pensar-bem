import math
import random

import matplotlib.pyplot as plt

from acervo import acervo_do_ivo
from resumo import desvio_padrao, media

discos = acervo_do_ivo(1971)
prateleiras = [v for v in discos if v < 300]
N = len(prateleiras)
verdade = sum(prateleiras)       # só a simulação sabe

random.seed(7)
estimativas = []
acertos = 0
for _ in range(2000):
    amostra = random.sample(prateleiras, 209)
    m = media(amostra)
    erro = desvio_padrao(amostra) / math.sqrt(209)
    estimativas.append(N * m)
    if abs(N * m - verdade) < 2 * N * erro:
        acertos += 1
print(f"valor real das prateleiras: R$ {verdade}")
print(f"faixas que contêm o valor real: {acertos / 2000:.3f}")

plt.figure(figsize=(6, 3.5))
plt.hist(estimativas, bins=40, color="0.85", edgecolor="0.4")
plt.axvline(verdade, color="black")
plt.xlabel("estimativa do valor das prateleiras (R$)")
plt.ylabel("amostras")
plt.savefig("estimativas.png", dpi=300, bbox_inches="tight")
