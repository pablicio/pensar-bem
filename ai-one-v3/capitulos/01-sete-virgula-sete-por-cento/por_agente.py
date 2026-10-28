import pandas as pd

from regra_jussara import carteira, regras_da_jussara

t = carteira()
t = t[t["data_concessao"].dt.year == 2025]
tabela = pd.DataFrame({
    "agente": t["agente"],
    "pela regra": regras_da_jussara(t).all(axis=1),
    "chegou a 90": t["data_atraso_90"].notna()})
resumo = tabela.groupby("agente").mean()
resumo = resumo.sort_values("pela regra")
print((resumo * 100).round(1).to_string())
