import numpy as np
import torch

from rio.avalia import erro_nos_picos, mae
from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.treino import conjunto, preve, treina

torch.manual_seed(0)
tab = com_subidas(tabela())
nivel = tab["cidade"]
escalada = Escala(tab).aplica(tab)
H = tuple(range(1, 13))
x, y, _ = conjunto(escalada, nivel, "treino", H, passo=2)
xv, yv, _ = conjunto(escalada, nivel, "validacao", H, passo=6)
modelo, _ = treina(Previsor(x.shape[2], H, estado=64),
                   x, y, xv, yv)
xt, yt, horas = conjunto(escalada, nivel, "teste", H)
p, yt = preve(modelo, xt), yt.numpy() / 10
erros = [mae(p[:, k] - yt[:, k]) * 100 for k in range(12)]
picos = erro_nos_picos(nivel, p[:, 11], horas, 12)
np.save("direta.npy", erros)
np.save("direta_prev.npy", p)
print("MAE por horizonte (cm):")
print(" ".join(f"{e:.2f}" for e in erros))
print(f"picos em 12 h: {np.mean(picos):.2f} m")
