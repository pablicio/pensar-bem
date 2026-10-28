import time

import numpy as np
import torch

from rio.avalia import erro_nos_picos, mae
from rio.convolucao import Convolucional
from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.treino import conjunto, preve, treina

tab = com_subidas(tabela())
nivel = tab["cidade"]
escalada = Escala(tab).aplica(tab)
H = (6, 12)
x, y, _ = conjunto(escalada, nivel, "treino", H, passo=2)
xv, yv, _ = conjunto(escalada, nivel, "validacao", H, passo=6)
xt, yt, horas = conjunto(escalada, nivel, "teste", H)
yt = yt.numpy() / 10
MODELOS = {
    "LSTM": lambda: Previsor(x.shape[2], H, estado=64),
    "convolucional": lambda: Convolucional(x.shape[2], H)}
print("modelo        parâm. épocas s/época  MAE 6 h  12 h"
      "  picos 12 h  2008")
for nome, cria in MODELOS.items():
    torch.manual_seed(0)
    modelo = cria()
    inicio = time.time()
    modelo, historico = treina(modelo, x, y, xv, yv)
    por_epoca = (time.time() - inicio) / len(historico)
    p = preve(modelo, xt)
    erros = [mae(p[:, j] - yt[:, j]) * 100 for j in range(2)]
    picos = erro_nos_picos(nivel, p[:, 1], horas, 12)
    total = sum(q.numel() for q in modelo.parameters())
    print(f"{nome:13} {total:6d} {len(historico):6d}"
          f" {por_epoca:7.1f} {erros[0]:7.2f} {erros[1]:5.2f}"
          f" {np.mean(picos):10.2f} {picos[0]:5.2f}")
    torch.save(modelo.state_dict(), f"{nome[:4]}_rio.pt")
print("alcance da convolucional:", modelo.alcance, "horas")
