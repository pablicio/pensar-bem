import torch

from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.quantis import QUANTIS, treina_quantis
from rio.treino import conjunto

torch.manual_seed(0)
tab = com_subidas(tabela())
nivel = tab["cidade"]
escalada = Escala(tab).aplica(tab)
H = tuple(range(1, 13))
x, y, _ = conjunto(escalada, nivel, "treino", H, passo=2)
xv, yv, _ = conjunto(escalada, nivel, "validacao", H, passo=6)
modelo = Previsor(x.shape[2], range(len(H) * len(QUANTIS)),
                  estado=64)
modelo, historico = treina_quantis(modelo, x, y, xv, yv)
print(len(historico), "épocas; modelo salvo em plantao.pt")
torch.save(modelo.state_dict(), "plantao.pt")
