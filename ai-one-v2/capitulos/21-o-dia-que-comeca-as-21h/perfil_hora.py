import pandas as pd

from rateio.fuso import cocalzinho_local
from rateio.geracao import dias_do_mes
from rateio.leitura import ler_cocalzinho

dias = ["2027-01-31"] + dias_do_mes("2027-02") + ["2027-03-01"]
b = ler_cocalzinho(dias)
valores = b["energia_kwh"].clip(lower=0).to_numpy()
instantes = cocalzinho_local(b["inicio"])
serie = pd.Series(valores, index=instantes)
fev = serie[serie.index.month == 2]
por_hora = fev.resample("h").sum()
perfil = por_hora.groupby(por_hora.index.hour).mean()
print(perfil.loc[5:19].round(0).to_string())
tarde = perfil.loc[16:].sum() / perfil.sum()
print(f"das 16h em diante: {tarde:.1%} da geração do dia")
