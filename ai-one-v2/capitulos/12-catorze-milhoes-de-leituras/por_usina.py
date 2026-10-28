import numpy as np

energia = np.load("dados/processados/leituras_ano.npy")
corumba = np.nansum(energia[:64]) / 1000 / 1000
cocalzinho = np.nansum(energia[64:110]) / 1000
abadiania = np.nansum(energia[110:]) / 1000
for nome, mwh in [("Corumbá de Goiás", corumba),
                  ("Cocalzinho", cocalzinho),
                  ("Abadiânia", abadiania)]:
    print(f"{nome:17} {mwh:9.3f} MWh")
total = corumba + cocalzinho + abadiania
print(f"total             {total:9.3f} MWh")
