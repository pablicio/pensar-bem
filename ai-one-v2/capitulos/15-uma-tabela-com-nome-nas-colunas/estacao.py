import pandas as pd

estacao = pd.read_csv("dados/brutos/estacao_corumba.csv")
print(estacao.shape)
print(estacao[["irradiancia_w_m2", "chuva_mm"]].describe()
      .round(1))
