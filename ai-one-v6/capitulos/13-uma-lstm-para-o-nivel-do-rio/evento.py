import matplotlib.pyplot as plt
import numpy as np
import torch

from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.treino import conjunto, preve

tab = com_subidas(tabela())
nivel = tab["cidade"]
escalada = Escala(tab).aplica(tab)
H = (6, 12)
modelo = Previsor(escalada.shape[1], H, estado=64)
modelo.load_state_dict(torch.load("lstm_rio.pt"))
xt, _, horas = conjunto(escalada, nivel, "teste", H)
variacao = preve(modelo, xt)[:, 1]
prevista = nivel.loc[horas].to_numpy() + variacao
# a previsão feita às t horas vale para t + 12
prevista = dict(zip(horas + np.timedelta64(12, "h"), prevista))
trecho = nivel.loc["2023-11-16":"2023-11-21"]
lstm = [prevista.get(h, np.nan) for h in trecho.index]
persistencia = nivel.shift(12).loc[trecho.index]
fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.plot(trecho.index, trecho, color="black", lw=1.6,
        label="observado")
ax.plot(trecho.index, persistencia, color="0.6", ls="--",
        label="persistência, 12 h antes")
ax.plot(trecho.index, lstm, color="#2A5F9E",
        label="LSTM, 12 h antes")
ax.axhline(5.5, color="#C0392B", lw=0.8, ls=":")
ax.set_ylabel("nível na régua (m)")
ax.tick_params(axis="x", labelsize=7, rotation=30)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("evento.png", dpi=300)
pico = trecho.idxmax()
print(f"pico: {trecho.max():.2f} m em {pico:%d/%m %Hh}")
print(f"LSTM, 12 h antes: {prevista[pico]:.2f} m")
print(f"persistência, 12 h antes: {persistencia[pico]:.2f} m")
