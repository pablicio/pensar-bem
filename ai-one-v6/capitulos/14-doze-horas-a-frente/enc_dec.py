import copy

import numpy as np
import torch
from torch import nn

from rio.avalia import erro_nos_picos, mae
from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import EncoderDecoder
from rio.treino import conjunto, preve

torch.manual_seed(0)
tab = com_subidas(tabela())
nivel = tab["cidade"]
escalada = Escala(tab).aplica(tab)
H = tuple(range(1, 13))
x, y, _ = conjunto(escalada, nivel, "treino", H, passo=2)
xv, yv, _ = conjunto(escalada, nivel, "validacao", H, passo=6)
# o alvo vira a variação de cada hora para a seguinte
passos = torch.diff(y, dim=1, prepend=torch.zeros(len(y), 1))
modelo = EncoderDecoder(x.shape[2], 12, estado=64)


class Acumula(nn.Module):
    """Soma as variações de cada hora: a previsão em cada
    horizonte, como as das outras estratégias."""

    def __init__(self, rede):
        super().__init__()
        self.rede = rede

    def forward(self, x):
        return torch.cumsum(self.rede(x), dim=1)


otimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
historico, melhor = [], None
for epoca in range(40):
    modelo.train()
    for i in torch.randperm(len(x)).split(256):
        previsto = modelo(x[i], alvo=passos[i])
        acumulado = torch.cumsum(previsto, dim=1)
        erro = nn.functional.mse_loss(acumulado, y[i])
        otimizador.zero_grad()
        erro.backward()
        nn.utils.clip_grad_norm_(modelo.parameters(), 1.0)
        otimizador.step()
    p = preve(Acumula(modelo), xv)
    historico.append(float(np.abs(p - yv.numpy() / 10).mean()))
    if historico[-1] == min(historico):
        melhor = copy.deepcopy(modelo.state_dict())
    elif epoca - int(np.argmin(historico)) >= 4:
        break
modelo.load_state_dict(melhor)
xt, yt, horas = conjunto(escalada, nivel, "teste", H)
p, yt = preve(Acumula(modelo), xt), yt.numpy() / 10
erros = [mae(p[:, k] - yt[:, k]) * 100 for k in range(12)]
picos = erro_nos_picos(nivel, p[:, 11], horas, 12)
np.save("enc_dec.npy", erros)
print("MAE por horizonte (cm):")
print(" ".join(f"{e:.2f}" for e in erros))
print(f"picos em 12 h: {np.mean(picos):.2f} m")
