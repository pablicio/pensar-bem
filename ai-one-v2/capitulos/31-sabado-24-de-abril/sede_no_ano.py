import pandas as pd

from rateio.leitura import BRUTOS
from rateio.reconciliacao import SEDE

total = 0.0
for mes in pd.period_range("2026-03", "2027-01", freq="M"):
    arquivo = BRUTOS / f"ged/compensacao/compensacao_{mes}.csv"
    ged = pd.read_csv(arquivo, sep=";", encoding="latin-1",
                      decimal=",", thousands=".")
    valor = ged.loc[ged["Nome"] == SEDE, "Valor (R$)"].iloc[0]
    total += valor
    print(f"{mes}  R$ {valor:5.2f}")
print(f"no ano: R$ {total:.2f}")
