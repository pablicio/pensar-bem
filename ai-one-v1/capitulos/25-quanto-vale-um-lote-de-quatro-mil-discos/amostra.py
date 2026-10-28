import math

from acervo import acervo_do_ivo
from resumo import desvio_padrao, media

discos = acervo_do_ivo(1971)
vidro = [v for v in discos if v >= 300]  # a estante de vidro
prateleiras = [v for v in discos if v < 300]  # o resto

amostra = prateleiras[::20]  # um disco a cada vinte
n, N = len(amostra), len(prateleiras)
m = media(amostra)
erro = desvio_padrao(amostra) / math.sqrt(n)
print(f"estante de vidro: {len(vidro)} discos,"
      f" R$ {sum(vidro)}")
print(f"amostra: {n} de {N} discos, média R$ {m:.2f}, "
      f"erro padrão R$ {erro:.2f}")
baixo, alto = N * (m - 2 * erro), N * (m + 2 * erro)
print(f"prateleiras: entre R$ {baixo:.0f} e R$ {alto:.0f}")
print(f"lote: entre R$ {sum(vidro) + baixo:.0f} "
      f"e R$ {sum(vidro) + alto:.0f}")
