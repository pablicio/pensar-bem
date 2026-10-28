import numpy as np

from rio.alerta import custo, limiar, maximo_previsto
from rio.avalia import parte
from rio.cota import julga
from rio.entradas import Escala, com_subidas, tabela
from rio.treino import conjunto

tab = com_subidas(tabela())
nivel = tab["cidade"]
H = tuple(range(1, 13))
escalada = Escala(tab).aplica(tab)
_, _, horas = conjunto(escalada, nivel, "teste", H)
quantis = np.load("quantis.npy")
agora = nivel.loc[horas].to_numpy()
print(f"limiar de Bayes: alarme se a chance passar de"
      f" {limiar():.1%}")
politicas = {f"quantil {q}": maximo_previsto(agora, quantis, k)
             for k, q in enumerate(("5%", "50%", "95%"))}
# a regra de 2006, como se fosse uma previsão "acima da cota"
teste = parte(nivel, "teste")
regra = (teste.diff() > 0.30).rolling(3).sum() == 3
regra = regra.reindex(horas, fill_value=False).to_numpy()
politicas["regra de 2006"] = np.where(regra, 99.0, 0.0)
print("política        a tempo  tarde  perdidas falsos custo")
for nome, maximo in politicas.items():
    cheias, ant, alarmes, falsos = julga(nivel, maximo, horas)
    tempo = sum(a >= 6 for a in ant)
    tarde = len(ant) - tempo
    perdidas = cheias - len(ant)
    print(f"{nome:15} {tempo:7d} {tarde:6d} {perdidas:9d}"
          f" {falsos:6d} {custo(ant, cheias, falsos):5.2f}")
