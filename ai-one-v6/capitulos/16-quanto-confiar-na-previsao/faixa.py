import matplotlib.pyplot as plt
import numpy as np

from rio.entradas import Escala, com_subidas, tabela
from rio.treino import conjunto

tab = com_subidas(tabela())
nivel = tab["cidade"]
H = tuple(range(1, 13))
escalada = Escala(tab).aplica(tab)
_, _, horas = conjunto(escalada, nivel, "teste", H)
p = np.load("quantis.npy")[:, 11]            # doze horas antes
alvo = horas + np.timedelta64(12, "h")       # vale para t + 12
faixa = nivel.loc[horas].to_numpy()[:, None] + p
faixa = dict(zip(alvo, faixa))
cheias = [("novembro de 2023", "2023-11-16", "2023-11-21"),
          ("novembro de 2008", "2008-11-21", "2008-11-26")]
fig, eixos = plt.subplots(1, 2, figsize=(9, 3.2), sharey=True)
for ax, (titulo, inicio, fim) in zip(eixos, cheias):
    trecho = nivel.loc[inicio:fim]
    q = np.array([faixa.get(h, [np.nan] * 3)
                  for h in trecho.index])
    ax.fill_between(trecho.index, q[:, 0], q[:, 2],
                    color="#2A5F9E", alpha=0.25,
                    label="90%, 12 h antes")
    ax.plot(trecho.index, q[:, 1], color="#2A5F9E", lw=1,
            label="mediana, 12 h antes")
    ax.plot(trecho.index, trecho, color="black", lw=1.5,
            label="observado")
    ax.set_title(titulo, fontsize=9)
    ax.tick_params(axis="x", labelsize=7, rotation=30)
    pico = trecho.idxmax()
    print(f"{titulo}: pico {trecho.max():.2f} m; 12 h antes,"
          f" de {faixa[pico][0]:.2f} a {faixa[pico][2]:.2f} m")
eixos[0].set_ylabel("nível na régua (m)")
eixos[0].legend(fontsize=7)
fig.tight_layout()
fig.savefig("faixa.png", dpi=300)
