import matplotlib.pyplot as plt
import pandas as pd

ano = pd.read_csv("dados/processados/geracao_diaria.csv")
b = ano[ano["usina"] == "Cocalzinho"]
diaria = b.groupby("data")["kwh"].sum() / 1000
diaria.index = pd.to_datetime(diaria.index)
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(diaria.index, diaria, color="0.7", label="dia")
ax.plot(diaria.index, diaria.rolling(30).mean(), color="0.1",
        label="média de 30 dias")
ax.set_ylabel("geração (MWh por dia)")
ax.legend()
fig.savefig("cocalzinho_ano.png", dpi=300, bbox_inches="tight")
print(round(diaria.max(), 1), round(diaria.min(), 1))
