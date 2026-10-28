from pathlib import Path

import pandas as pd

from rateio.geracao import dias_do_mes
from rateio.leitura import (ler_abadiania, ler_cocalzinho,
                            ler_corumba)
from rateio.limpeza import corumba_em_kwh

mes = "2027-03"
a = ler_corumba(mes)
b = ler_cocalzinho(dias_do_mes(mes))
c = ler_abadiania(mes)
leituras = pd.concat([
    pd.DataFrame({"usina": "Corumbá de Goiás",
                  "inversor": a["Inversor"],
                  "instante": a["Data"] + " " + a["Hora"],
                  "kwh": corumba_em_kwh(a)}),
    pd.DataFrame({"usina": "Cocalzinho",
                  "inversor": b["inversor"],
                  "instante": b["inicio"],
                  "kwh": b["energia_kwh"]}),
    pd.DataFrame({"usina": "Abadiânia",
                  "inversor": c["inverter"],
                  "instante": c["timestamp"],
                  "kwh": c["energy_kwh"]}),
], ignore_index=True)

memoria = leituras.memory_usage(deep=True) / 1e6
print(f"{len(leituras):,} leituras em março")
print(memoria.round(1).to_string())
print(f"total: {memoria.sum():.1f} MB")
destino = Path("dados/processados/leituras_marco.csv")
destino.parent.mkdir(exist_ok=True)
leituras.to_csv(destino, index=False)
print(f"em CSV: {destino.stat().st_size / 1e6:.1f} MB")
