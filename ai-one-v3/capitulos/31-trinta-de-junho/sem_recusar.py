import pandas as pd

from concedidos import concedidos, covenant

junho = pd.read_csv("dados/brutos/fechamento_cobranca.csv")
for nome, modelo in [("com o modelo", True),
                     ("aprovando todos", False)]:
    c = junho.merge(concedidos(modelo), on="pedido_id")
    print(f"{nome:16} em 30/06: {covenant(c):.2%}")
