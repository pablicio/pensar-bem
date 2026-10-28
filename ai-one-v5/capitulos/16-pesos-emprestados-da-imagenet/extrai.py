import time

import torch

from folha.conjunto import Folhas
from folha.emprestada import extrai, extratora
from folha.treino import fixar_semente

fixar_semente(0, nucleos=4)
rede = extratora()
matrizes = {}
for parte in ("treino", "validacao"):
    inicio = time.time()
    x, y = extrai(rede, Folhas(parte))
    matrizes[parte] = (x, y)
    segundos = time.time() - inicio
    print(f"{parte:9} {tuple(x.shape)} em {segundos:.0f} s")
torch.save(matrizes, "caracteristicas.pt")
