import numpy as np
import pandas as pd

from pedido_da_cida import pedido_da_cida
from primeiro_modelo import FINANCEIRAS, primeiro_modelo
from risco.dados import tabela, treino_validacao

treino, _ = treino_validacao(tabela())
modelo = primeiro_modelo(treino)
escala, logistica = modelo[0], modelo[-1]
cida = pedido_da_cida()

x = cida[FINANCEIRAS].to_numpy()[0]
z = (x - escala.mean_) / escala.scale_
parcela = pd.DataFrame({"dela": x, "padronizado": z,
                        "peso": logistica.coef_[0],
                        "soma": logistica.coef_[0] * z},
                       index=FINANCEIRAS)
print(parcela.sort_values("soma", ascending=False).round(2))
total = logistica.intercept_[0] + parcela["soma"].sum()
print(f"\nintercepto {logistica.intercept_[0]:.2f}"
      f" + soma {parcela['soma'].sum():.2f} = {total:.2f}")
print(f"probabilidade: {1 / (1 + np.exp(-total)):.1%}")
