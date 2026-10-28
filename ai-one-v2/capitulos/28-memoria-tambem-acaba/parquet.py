import time
from pathlib import Path

import pandas as pd

from rateio.leituras import leituras_do_mes

leituras = leituras_do_mes("2027-03")
destino = Path("dados/processados/leituras_marco.parquet")
leituras.to_parquet(destino)
print(f"em Parquet: {destino.stat().st_size / 1e6:.1f} MB")

de_volta = pd.read_parquet(destino)
iguais = (de_volta.dtypes == leituras.dtypes).all()
print("mesmos tipos:", iguais)
print("mesmos dados:", de_volta.equals(leituras))

for arquivo in ["leituras_marco.csv",
                "leituras_marco.parquet"]:
    caminho = Path("dados/processados") / arquivo
    inicio = time.perf_counter()
    if caminho.suffix == ".csv":
        pd.read_csv(caminho)
    else:
        pd.read_parquet(caminho)
    segundos = time.perf_counter() - inicio
    print(f"{arquivo:24} {segundos:.3f} s")
