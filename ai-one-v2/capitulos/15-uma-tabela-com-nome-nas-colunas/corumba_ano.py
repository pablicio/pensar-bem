from pathlib import Path

import pandas as pd

pasta = Path("dados/brutos/inversores/corumba")
partes = [pd.read_csv(caminho, sep=";", skiprows=1,
                      encoding="latin-1", decimal=",",
                      thousands=".")
          for caminho in sorted(pasta.glob("*.csv"))]
ano = pd.concat(partes, ignore_index=True)
print(ano.shape)
print(f"{ano.memory_usage(deep=True).sum() / 1e6:.0f} MB")
