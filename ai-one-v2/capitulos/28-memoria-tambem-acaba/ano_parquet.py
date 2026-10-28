from pathlib import Path

import pandas as pd

from rateio.leituras import leituras_do_mes

meses = pd.period_range("2026-03", "2027-02", freq="M")
ano = pd.concat([leituras_do_mes(str(mes)) for mes in meses],
                ignore_index=True)
destino = Path("dados/processados/leituras_ano.parquet")
ano.to_parquet(destino)
memoria = ano.memory_usage(deep=True).sum() / 1e6
print(f"{len(ano):,} leituras, {memoria:.0f} MB na memória")
print(f"tipos: {', '.join(str(t) for t in ano.dtypes)}")
print(f"em Parquet: {destino.stat().st_size / 1e6:.1f} MB")
