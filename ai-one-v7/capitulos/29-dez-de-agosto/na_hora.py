import time

import torch

from lauber.acervo import carrega, grade
from lauber.emenda import ladrilho
from lauber.vizinhos import carrega_npz, vizinho

inicio = time.perf_counter()
colecao = torch.load("vitrine.pt")      # as 20 do capítulo 28
acervo, _ = carrega()
pasta = carrega_npz("catalogo")         # a pasta da Renata
print("estampa  pasta da Renata   acervo da Lauber")
for numero, x in enumerate(colecao, start=1):
    q, s = vizinho(x[None], pasta, espelho=True)
    a, t = vizinho(x[None], acervo, espelho=True)
    print(f"{numero:7d} {int(q[0]):6d} {s[0]:.3f}"
          f" {int(a[0]):9d} {t[0]:.3f}")
segundos = time.perf_counter() - inicio
print(f"tudo conferido em {segundos:.1f} s")

# a escolhida da Renata, ao lado da vizinha dela no acervo
a, _ = vizinho(colecao[4:5], acervo, espelho=True)
grade(torch.stack([ladrilho(colecao[4]),
                   ladrilho(acervo[int(a[0])])]),
      "escolhida.png", colunas=2)
