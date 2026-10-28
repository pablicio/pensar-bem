import numpy as np

from rio.cota import julga
from rio.entradas import Escala, com_subidas, tabela
from rio.treino import conjunto

tab = com_subidas(tabela())
nivel = tab["cidade"]
H = tuple(range(1, 13))
escalada = Escala(tab).aplica(tab)
_, _, horas = conjunto(escalada, nivel, "teste", H)
agora = nivel.loc[horas].to_numpy()
print("perda   cota  cheias avisadas antes  alarmes falsos")
for nome in ("comum", "pesada"):
    maximo = agora + np.load(f"prev_{nome}.npy").max(axis=1)
    for cota in (4.0, 5.5, 7.0):
        cheias, ant, alarmes, falsos = julga(nivel, maximo,
                                             horas, cota)
        print(f"{nome:7} {cota:4.1f} {cheias:6d} {len(ant):8d}"
              f" {np.mean(ant):4.1f} h {alarmes:7d}"
              f" {falsos:6d}")
