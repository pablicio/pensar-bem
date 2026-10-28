import numpy as np
import torch

from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.quantis import QUANTIS, preve_quantis, treina_quantis
from rio.treino import conjunto

torch.manual_seed(0)
tab = com_subidas(tabela())
nivel = tab["cidade"]
escalada = Escala(tab).aplica(tab)
H = tuple(range(1, 13))
x, y, _ = conjunto(escalada, nivel, "treino", H, passo=2)
xv, yv, _ = conjunto(escalada, nivel, "validacao", H, passo=6)
saidas = range(len(H) * len(QUANTIS))
modelo = Previsor(x.shape[2], saidas, estado=64)
modelo, historico = treina_quantis(modelo, x, y, xv, yv)
print(len(historico), "épocas")
xt, yt, horas = conjunto(escalada, nivel, "teste", H)
p, yt = preve_quantis(modelo, xt), yt.numpy() / 10
np.save("quantis.npy", p)
agora = nivel.loc[horas].to_numpy()
alto = (agora[:, None] + yt).max(axis=1) >= 4.0
for k in (5, 11):
    baixo, alto_q = p[:, k, 0], p[:, k, 2]
    dentro = (yt[:, k] >= baixo) & (yt[:, k] <= alto_q)
    largura = (alto_q - baixo) * 100
    print(f"{k + 1:2d} h: cobertura {dentro.mean():.1%},"
          f" largura {largura.mean():.1f} cm")
    print(f"      acima de 4 m: {dentro[alto].mean():.1%},"
          f" {largura[alto].mean():.0f} cm")
