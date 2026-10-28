import numpy as np

energia = np.load("dados/processados/leituras_ano.npy")
faltas_dia = np.isnan(energia[110:]).sum(axis=(0, 2))
inicio_mes = [0, 31, 61, 92, 122, 153, 184, 214, 245, 275,
              306, 337, 365]
meses = ["mar", "abr", "mai", "jun", "jul", "ago", "set",
         "out", "nov", "dez", "jan", "fev"]
for nome, a, b in zip(meses, inicio_mes, inicio_mes[1:]):
    total = int(faltas_dia[a:b].sum())
    if total:
        print(nome, total, "leituras faltando")
