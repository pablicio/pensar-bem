from datetime import date, timedelta

import numpy as np

energia = np.load("dados/processados/leituras_ano.npy")
energia[:64] /= 1000                 # fabricante A: Wh -> kWh
energia[energia < 0] = 0             # consumo noturno não gera

diario = np.nansum(energia, axis=2)  # kWh por inversor e dia
np.save("dados/processados/diario.npy", diario)
print("tabela da auditoria:", diario.shape)

usinas = {"Corumbá de Goiás": diario[:64],
          "Cocalzinho": diario[64:110],
          "Abadiânia": diario[110:]}
for nome, bloco in usinas.items():
    por_dia = bloco.sum(axis=0)
    print(f"{nome:17} {por_dia.sum() / 1000:7.1f} MWh, "
          f"melhor dia {por_dia.max():6.0f} kWh")

corumba = usinas["Corumbá de Goiás"].sum(axis=0)
for i in np.argsort(corumba)[:3]:
    quando = date(2026, 3, 1) + timedelta(days=int(i))
    print("dia mais fraco:", quando,
          round(float(corumba[i]), 1))
