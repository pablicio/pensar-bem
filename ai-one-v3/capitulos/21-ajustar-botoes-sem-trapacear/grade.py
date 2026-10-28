import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import PredefinedSplit

from botoes import COL
from risco.dados import lacrar, tabela, treino_validacao
from risco.finalidade import com_divida
from risco.modelos import boosting

aberto, _ = lacrar(com_divida(tabela()))
treino, valid = treino_validacao(aberto)
dobra = np.where(aberto.index.isin(valid.index), 0, -1)

grade = {"modelo__max_depth": [1, 2, 3],
         "modelo__learning_rate": [0.05, 0.1, 0.2]}
busca = GridSearchCV(boosting(iteracoes=325), grade,
                     scoring="roc_auc",
                     cv=PredefinedSplit(dobra))
busca.fit(aberto[COL], aberto["alvo"])

r = pd.DataFrame(busca.cv_results_["params"])
r.columns = ["taxa", "profundidade"]
r["AUC"] = busca.cv_results_["mean_test_score"].round(3)
print(r.pivot(index="profundidade", columns="taxa",
              values="AUC"))
