import numpy as np

from dados.bacia import reservatorio
from rio.serie import ler

chuva = ler("telemetria")["apiuna"]
chuva = chuva.loc["2008-11-12":"2008-11-25"].fillna(0)
chuva = chuva.to_numpy()
k = 4.0
h = 0.0
estados = []
for x in chuva:                   # o reservatório, hora a hora
    h = (1 - 1 / k) * h + (1 / k) * x
    estados.append(h)
pronto = reservatorio(chuva, k)   # o do apêndice A3
print(len(chuva), "horas de chuva em Apiúna")
diferenca = np.abs(np.array(estados) - pronto).max()
print("maior diferença:", diferenca)
