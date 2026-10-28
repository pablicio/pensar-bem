from pathlib import Path

import pandas as pd

from rateio.geracao import geracao_diaria

meses = [f"2026-{m:02d}" for m in range(3, 13)]
meses += ["2027-01", "2027-02"]
ano = pd.concat([geracao_diaria(mes) for mes in meses],
                ignore_index=True)
saida = Path("dados/processados")
saida.mkdir(parents=True, exist_ok=True)
ano.to_csv(saida / "geracao_diaria.csv", index=False)

ano["mes"] = ano["data"].str[:7]
tabela = ano.pivot_table(index="mes", columns="usina",
                         values="kwh", aggfunc="sum",
                         margins=True, margins_name="total")
mwh = (tabela / 1000).round(1)
print(mwh.to_string())
print(f"soma das leituras: {ano['kwh'].sum() / 1000:.1f} MWh")
