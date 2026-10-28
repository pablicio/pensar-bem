import pandas as pd

ano = pd.read_csv("dados/processados/geracao_diaria.csv")
por_usina_dia = ano.groupby(["usina", "data"])["kwh"]
media_dia = por_usina_dia.transform("mean")
fracos = ano[ano["kwh"] < media_dia / 2]
print(fracos.groupby("usina").size())
print(fracos.groupby("usina")["inversor"].nunique())
