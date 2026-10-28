import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import torch

from rio.entradas import Escala, com_subidas, tabela
from rio.espera import PlantaoComEspera
from rio.estacoes import ESTACOES, colunas_de
from rio.modelos import Previsor
from rio.serie import ler

HORA = pd.Timedelta("1h")
tele = ler("temporada_2027")
historico = com_subidas(tabela())


def rede(arquivo, tab):
    modelo = Previsor(tab.shape[1], range(36), estado=64)
    modelo.load_state_dict(torch.load(arquivo))
    return modelo, Escala(tab)


reservas = {}
for e in ESTACOES:
    sem = historico.drop(columns=colunas_de(e))
    reservas[e] = rede(f"sem_{e}.pt", sem)
plantao = PlantaoComEspera(*rede("plantao.pt", historico),
                           historico, reservas)
horas = pd.date_range("2027-10-05", "2027-10-16", freq="h")
registro = pd.DataFrame([plantao.hora(tele.loc[:h])
                         for h in horas]).set_index("hora")
registro.to_csv("registro_outubro.csv")
nivel = registro["nivel"]
for hora, nota in registro["nota"].items():
    if nota:
        print(f"{hora:%d/%m %Hh}  nível {nivel[hora]:.2f} m:"
              f" {nota[:34]}")
passou = nivel.index[nivel >= 5.5][0]
pico = nivel.idxmax()
antes = registro.loc[pico - 12 * HORA]
print(f"o rio passou de 5,5 m em {passou:%d/%m %Hh};"
      f" pico de {nivel[pico]:.2f} m em {pico:%d/%m %Hh}")
print(f"12 h antes do pico: mediana {antes['mediana']:.2f} m,"
      f" teto {antes['teto']:.2f} m")
fora = registro.index[registro["fora"].fillna("") != ""]
print(f"estação fora: {registro.loc[fora[0], 'fora']},"
      f" {fora[0]:%d/%m %Hh} a {fora[-1]:%d/%m %Hh}")
chamou = registro.index[registro["chamada"]]
print("chamadas ao Major:",
      " ".join(f"{h:%d/%m %Hh}" for h in chamou))
# a regra de 2006: subir mais de 30 cm/h por 3 horas
regra = (nivel.diff() > 0.30).rolling(3).sum() == 3
disparos = [f"{h:%d/%m %Hh}" for h in nivel.index[regra]]
print("a regra de 2006 dispararia:",
      " ".join(disparos) or "nunca")
fig, ax = plt.subplots(figsize=(7, 3.2))
ax.plot(nivel.index, nivel, color="black", label="nível")
ax.plot(registro.index, registro["teto"], color="#c33",
        lw=1, label="teto previsto para 12 h")
ax.plot(registro.index, registro["mediana"], color="#36a",
        lw=1, label="mediana prevista para 12 h")
ax.axhline(5.5, color="gray", ls=":", lw=1)
ax.set_ylabel("metros")
ax.legend(loc="upper left", fontsize=8)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
fig.tight_layout()
fig.savefig("outubro.png", dpi=300)
