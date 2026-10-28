import pandas as pd

from primeiro_modelo import FINANCEIRAS, primeiro_modelo
from risco.dados import com_variaveis, tabela, treino_validacao

treino, valid = treino_validacao(tabela())
modelo = primeiro_modelo(treino)

e = pd.read_csv("dados/brutos/emprestimos.csv")
cida = com_variaveis(e[e["cliente_id"] == "C00000"].tail(1))
p = modelo.predict_proba(cida[FINANCEIRAS])[0, 1]
p_valid = modelo.predict_proba(valid[FINANCEIRAS])[:, 1]
acima = (p_valid < p).mean()
print(f"Dona Cida: probabilidade de chegar a 90 dias: {p:.1%}")
print(f"mais arriscada que {acima:.0%} dos empréstimos"
      " da validação")
corte = pd.Series(p_valid).quantile(0.90)
print(f"recusando os 10% mais arriscados (p > {corte:.1%}):"
      f" {'recusa' if p > corte else 'aprova'}")
