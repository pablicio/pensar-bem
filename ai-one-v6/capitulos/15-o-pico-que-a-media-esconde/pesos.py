import numpy as np
import torch

from rio.avalia import erro_nos_picos, mae
from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.treino import conjunto, preve, treina

tab = com_subidas(tabela())
nivel = tab["cidade"]
escalada = Escala(tab).aplica(tab)
H = tuple(range(1, 13))
x, y, horas_tr = conjunto(escalada, nivel, "treino", H,
                          passo=2)
xv, yv, _ = conjunto(escalada, nivel, "validacao", H, passo=6)
xt, yt, horas = conjunto(escalada, nivel, "teste", H)
yt = yt.numpy() / 10
# o nível mais alto das próximas 12 horas de cada exemplo
agora = torch.tensor(nivel.loc[horas_tr].to_numpy(),
                     dtype=torch.float32)
alto = (agora[:, None] + y / 10).max(dim=1).values >= 4.0
print(f"exemplos que passam de 4 m: {int(alto.sum())}"
      f" de {len(alto)}")
print("perda     MAE 6 h  MAE 12 h  picos 12 h")
for nome, pesos in (("comum", None),
                    ("pesada", 1 + 9 * alto.float())):
    torch.manual_seed(0)
    modelo, _ = treina(Previsor(x.shape[2], H, estado=64),
                       x, y, xv, yv, pesos=pesos)
    p = preve(modelo, xt)
    np.save(f"prev_{nome}.npy", p)
    picos = erro_nos_picos(nivel, p[:, 11], horas, 12)
    print(f"{nome:8} {mae(p[:, 5] - yt[:, 5]) * 100:7.2f}"
          f" {mae(p[:, 11] - yt[:, 11]) * 100:9.2f}"
          f" {np.mean(picos):10.2f}")
