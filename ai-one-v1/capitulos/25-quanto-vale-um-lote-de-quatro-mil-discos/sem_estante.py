import math
import random

from acervo import acervo_do_ivo
from resumo import desvio_padrao, media

discos = acervo_do_ivo(1971)
verdade = sum(discos)
random.seed(7)
acertos = 0
for _ in range(2000):
    amostra = random.sample(discos, 209)
    m = media(amostra)
    erro = desvio_padrao(amostra) / math.sqrt(209)
    if abs(4200 * m - verdade) < 2 * 4200 * erro:
        acertos += 1
print(f"faixas que contêm o valor real: {acertos / 2000:.3f}")
