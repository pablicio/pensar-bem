import pandas as pd

arquivo = "dados/processados/leituras_marco.csv"
soma = pd.Series(0.0, index=["Corumbá de Goiás", "Cocalzinho",
                             "Abadiânia"])
pedacos = 0
for pedaco in pd.read_csv(arquivo, chunksize=200_000):
    pedacos += 1
    positivo = pedaco["kwh"].clip(lower=0)
    soma = soma.add(positivo.groupby(pedaco["usina"]).sum(),
                    fill_value=0)
print(pedacos, "pedaços de até 200.000 linhas")
print(soma.round(1).to_string())
