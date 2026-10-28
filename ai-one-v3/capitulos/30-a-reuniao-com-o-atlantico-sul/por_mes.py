import pandas as pd

from politicas import politicas

teste, valores, regras = politicas()
mes = teste["data_concessao"].dt.strftime("%m/%Y").to_numpy()
alvo = teste["alvo"].to_numpy()
jussara, _, modelo, _ = regras.values()

linhas = []
for m in pd.unique(mes):
    s = mes == m
    linhas.append({
        "mês": m,
        "inad. regra": alvo[s & jussara].mean(),
        "inad. modelo": alvo[s & modelo].mean(),
        "lucro regra": valores[s & jussara].sum(),
        "lucro modelo": valores[s & modelo].sum()})
tabela = pd.DataFrame(linhas).set_index("mês")
print(tabela.to_string(formatters={
    "inad. regra": "{:.1%}".format,
    "inad. modelo": "{:.1%}".format,
    "lucro regra": "{:,.0f}".format,
    "lucro modelo": "{:,.0f}".format}))
