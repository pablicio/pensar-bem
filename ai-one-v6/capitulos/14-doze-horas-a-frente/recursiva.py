import numpy as np
import torch

from rio.avalia import erro_nos_picos, mae
from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.recursiva import rola
from rio.treino import conjunto, treina

torch.manual_seed(0)
tab = com_subidas(tabela())
nivel = tab["cidade"]
escala = Escala(tab)
escalada = escala.aplica(tab)
H = tuple(range(1, 13))
x, y, _ = conjunto(escalada, nivel, "treino", (1,), passo=2)
xv, yv, _ = conjunto(escalada, nivel, "validacao", (1,),
                     passo=6)
modelo, _ = treina(Previsor(x.shape[2], (1,), estado=64),
                   x, y, xv, yv)
xt, yt, horas = conjunto(escalada, nivel, "teste", H)
p = np.concatenate([rola(modelo, xt[i:i + 4096], escala, 12)
                    for i in range(0, len(xt), 4096)])
yt = yt.numpy() / 10
erros = [mae(p[:, k] - yt[:, k]) * 100 for k in range(12)]
picos = erro_nos_picos(nivel, p[:, 11], horas, 12)
np.save("recursiva.npy", erros)
print("MAE por horizonte (cm):")
print(" ".join(f"{e:.2f}" for e in erros))
print(f"picos em 12 h: {np.mean(picos):.2f} m")
