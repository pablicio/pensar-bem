import pandas as pd

cad = pd.read_excel("dados/brutos/cadastro_cooperados.xlsx")
ativos = cad[cad["Situação"] == "Ativo"]
for tipo in ["residencial", "comercio", "rural"]:
    consumo = ativos.loc[ativos["Tipo"] == tipo,
                         "Consumo médio (kWh)"]
    zeros = int((consumo == 0).sum())
    com = consumo.mean()
    sem = consumo.replace(0, pd.NA).mean()
    print(f"{tipo:12} {zeros:3} zeros  {com:7.1f} -> "
          f"{sem:7.1f} kWh")
