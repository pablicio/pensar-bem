import random

from acervo import acervo_do_ivo
from resumo import desvio_padrao, media

prateleiras = [v for v in acervo_do_ivo(1971) if v < 300]
N = len(prateleiras)
for n in [50, 209, 800]:
    random.seed(8)
    est = [N * media(random.sample(prateleiras, n))
           for _ in range(2000)]
    print(f"amostra de {n}: desvio das estimativas "
          f"R$ {desvio_padrao(est):.0f}")
