import numpy as np
import torch

from rio.avalia import erro_nos_picos, mae
from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.reserva import com_reserva, fora_da_faixa
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
fora = fora_da_faixa(tab)
q = com_reserva(p, nivel, horas, fora)
np.save("rede.npy", p)
np.save("reserva.npy", q)
dentro = fora.loc[horas]
lista = horas[dentro.to_numpy()].strftime("%m/%Y")
meses = dict.fromkeys(lista)            # sem repetir, em ordem
print("horas fora da faixa no teste:", int(dentro.sum()))
print("em", ", ".join(meses))
print("           MAE 12 h   picos 12 h   2008    2023-11")
for nome, prev in (("rede", p), ("com reserva", q)):
    pk = erro_nos_picos(nivel, prev[:, 11], horas, 12)
    erro = mae(prev[:, 11] - yt[:, 11]) * 100
    print(f"{nome:11} {erro:7.2f} {np.mean(pk):11.2f}"
          f" {pk[0]:8.2f} {pk[4]:8.2f}")
