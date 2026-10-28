import pandas as pd

from risco.dados import tabela, treino_validacao

treino, _ = treino_validacao(tabela())
limites = [18, 22, 25, 30, 40, 50, 60, 65, 80]
faixas = pd.cut(treino["idade"], limites)
taxa = treino.groupby(faixas, observed=True)["alvo"].mean()
print((taxa * 100).round(1).to_string())
