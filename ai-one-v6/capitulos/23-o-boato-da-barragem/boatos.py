import pandas as pd

from rio.texto import mensagens

tab = mensagens()
tarde = tab[(tab["data_hora"] >= "2023-11-18 15:00")
            & (tab["data_hora"] < "2023-11-18 21:00")]
hora = tarde["data_hora"].dt.floor("h")
por_hora = pd.crosstab(hora, tarde["verdade"])
por_hora.index = por_hora.index.strftime("%Hh")
print(por_hora[["risco", "ajuda", "info", "boato"]])
TIPOS = {"barragem": "barragem|comporta",
         "ponte de ferro": "ponte de ferro rachou",
         "exército": "evacuar a cidade",
         "falta de água": "quinze dias"}
boato = tab[tab["verdade"] == "boato"]["texto"]
print(f"os {len(boato)} boatos do arquivo:")
for nome, padrao in TIPOS.items():
    n = boato.str.contains(padrao).sum()
    print(f"  {nome:15} {n:5d}")
disfarce = boato.str.contains("pedindo socorro")
print(f"  disfarçados de pedido ('estão pedindo socorro'):"
      f" {disfarce.sum()}")
