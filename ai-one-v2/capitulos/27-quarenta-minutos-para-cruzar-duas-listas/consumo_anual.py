from pathlib import Path

import pandas as pd

from rateio.limpeza import cpf_normalizado

pasta = Path("dados/brutos/ged/consumo")
meses = pd.period_range("2026-03", "2027-02", freq="M")
partes = [pd.read_csv(pasta / f"consumo_{mes}.csv",
                      dtype={"cpf": "string"})
          for mes in meses]
consumo = pd.concat(partes, ignore_index=True)
consumo["cpf"] = cpf_normalizado(consumo["cpf"])
anual = consumo.groupby("cpf")["kwh"].sum().round(2)
print(f"{len(consumo):,} linhas, {len(anual):,} cooperados")
print(f"Seu Dirceu: {anual['06041976598']:,.2f} kWh no ano")
Path("dados/processados").mkdir(exist_ok=True)
anual.to_csv("dados/processados/consumo_anual.csv")
