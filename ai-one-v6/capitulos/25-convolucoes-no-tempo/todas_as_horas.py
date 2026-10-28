import time

import numpy as np
import torch

from rio.avalia import parte
from rio.convolucao import Convolucional
from rio.entradas import Escala, com_subidas, tabela
from rio.treino import conjunto, preve

tab = com_subidas(tabela())
nivel = tab["cidade"]
escalada = Escala(tab).aplica(tab)
H = (6, 12)
xt, _, horas = conjunto(escalada, nivel, "teste", H)
modelo = Convolucional(xt.shape[2], H)
modelo.load_state_dict(torch.load("conv_rio.pt"))
inicio = time.time()
por_janela = preve(modelo, xt)
segundos = time.time() - inicio
print(f"{len(xt)} janelas de 72 h: {segundos:.1f} s")
serie = parte(escalada, "teste").to_numpy(dtype=float)
z = torch.tensor(np.nan_to_num(serie), dtype=torch.float32)
inicio = time.time()
with torch.no_grad():
    todas = modelo.por_hora(z[None])[0].numpy() / 10
print(f"a série inteira, {len(serie)} horas, de uma vez:"
      f" {time.time() - inicio:.2f} s")
mesmas = parte(escalada, "teste").index.get_indexer(horas)
diferenca = np.abs(todas[mesmas] - por_janela).max()
print(f"maior diferença entre as duas: {diferenca:.0e} m")
