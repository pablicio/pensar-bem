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
H = (6, 12)
x, y, _ = conjunto(escalada, nivel, "treino", H, passo=2)
xv, yv, _ = conjunto(escalada, nivel, "validacao", H, passo=6)
print(f"{len(x)} janelas de treino, {x.shape[1]} horas,"
      f" {x.shape[2]} colunas")
modelo = Previsor(x.shape[2], H, estado=64)
modelo, historico = treina(modelo, x, y, xv, yv)
melhor = int(np.argmin(historico))
print(f"{len(historico)} épocas; a melhor foi a {melhor + 1},"
      f" com {historico[melhor] * 100:.2f} cm na validação")
torch.save(modelo.state_dict(), "lstm_rio.pt")
xt, yt, horas = conjunto(escalada, nivel, "teste", H)
p, yt = preve(modelo, xt), yt.numpy() / 10
for j, h in enumerate(H):
    picos = erro_nos_picos(nivel, p[:, j], horas, h)
    erro = mae(p[:, j] - yt[:, j]) * 100
    print(f"{h:2d} h: MAE {erro:.2f} cm,"
          f" picos {np.mean(picos):5.2f} m,"
          f" 2008 {picos[0]:5.2f} m")
