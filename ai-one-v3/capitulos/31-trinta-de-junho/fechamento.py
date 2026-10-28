import pandas as pd

from concedidos import concedidos, covenant

marco = pd.read_csv("dados/brutos/cobranca.csv")
junho = pd.read_csv("dados/brutos/fechamento_cobranca.csv")
junho = junho.merge(concedidos(), on="pedido_id")

for nome, c in [("12/03", marco), ("30/06", junho)]:
    ativa = c[c["situacao"].isin(["em dia", "atraso"])]
    saldo = ativa["saldo_devedor"].sum()
    print(f"{nome}: carteira de R$ {saldo:,.0f},"
          f" inadimplência {covenant(c):.2%}")
print("covenant: abaixo de 6.50%")
