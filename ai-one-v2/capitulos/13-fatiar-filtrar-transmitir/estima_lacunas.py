import numpy as np

energia = np.load("dados/processados/leituras_ano.npy")
falta = np.isnan(energia[110])         # buracos: iguais nos 30
b = np.clip(energia[64:110], 0, None)  # Cocalzinho, sem < 0
por_kw = b.sum(axis=0) / 1800          # kWh por kW
estimado = (por_kw[falta] * 1200).sum()
print(f"{falta.sum()} intervalos sem leitura")
print(f"estimativa: {estimado:,.0f} kWh")
