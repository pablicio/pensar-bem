import numpy as np
import pandas as pd

from concedidos import concedidos

junho = pd.read_csv("dados/brutos/fechamento_cobranca.csv")
junho = junho.merge(concedidos(), on="pedido_id")
ativa = junho[junho["situacao"].isin(["em dia", "atraso"])]
ruim = np.where(ativa["dias_atraso_atual"] > 90,
                ativa["saldo_devedor"], 0)
safra = ativa["data_concessao"].dt.to_period("Q")

t = pd.DataFrame({"saldo": ativa["saldo_devedor"],
                  "ruim": ruim})
t = t.groupby(safra.rename("safra")).sum()
t["parte do ruim"] = t["ruim"] / t["ruim"].sum()
formatos = {"saldo": "{:,.0f}".format,
            "ruim": "{:,.0f}".format,
            "parte do ruim": "{:.1%}".format}
print(t.to_string(formatters=formatos))
