import pandas as pd

from experimento import credito_kwh, monta_tabela
from rateio.calculo import TARIFA

tabela = monta_tabela()
reais = pd.DataFrame({
    "tipo": tabela["tipo"],
    "cota": (credito_kwh(tabela, 0) * TARIFA).round(2),
    "consumo": (credito_kwh(tabela, 1) * TARIFA).round(2)})
por_tipo = reais.groupby("tipo")[["cota", "consumo"]].sum()
por_tipo["diferença"] = por_tipo["consumo"] - por_tipo["cota"]
print((por_tipo / 1000).round(1).to_string())
