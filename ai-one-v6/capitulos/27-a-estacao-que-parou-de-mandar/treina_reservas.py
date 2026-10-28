import torch

from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.estacoes import ESTACOES, colunas_de
from rio.quantis import QUANTIS, treina_quantis
from rio.treino import conjunto

tab = com_subidas(tabela())
nivel = tab["cidade"]
H = tuple(range(1, 13))
for estacao in ESTACOES:
    sem = tab.drop(columns=colunas_de(estacao))
    escalada = Escala(sem).aplica(sem)
    x, y, _ = conjunto(escalada, nivel, "treino", H, passo=2)
    xv, yv, _ = conjunto(escalada, nivel, "validacao", H,
                         passo=6)
    torch.manual_seed(0)
    modelo = Previsor(x.shape[2], range(len(H) * len(QUANTIS)),
                      estado=64)
    modelo, historico = treina_quantis(modelo, x, y, xv, yv)
    print(f"sem {estacao}: {x.shape[2]} colunas,"
          f" {len(historico)} épocas")
    torch.save(modelo.state_dict(), f"sem_{estacao}.pt")
