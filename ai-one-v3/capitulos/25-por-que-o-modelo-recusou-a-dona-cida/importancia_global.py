import pandas as pd
from sklearn.inspection import permutation_importance

from risco.campeao import COLUNAS_FINAIS, treinado
from risco.dados import lacrar, tabela
from risco.finalidade import com_divida

modelo = treinado()
aberto, _ = lacrar(com_divida(tabela()))
r = permutation_importance(modelo, aberto[COLUNAS_FINAIS],
                           aberto["alvo"], scoring="roc_auc",
                           n_repeats=5, random_state=0)
perda = pd.Series(r.importances_mean, COLUNAS_FINAIS)
print("perda de AUC ao embaralhar")
print(perda.sort_values(ascending=False).round(4).to_string())
