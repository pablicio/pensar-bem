import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from primeiro_modelo import FINANCEIRAS
from risco.dados import com_variaveis, tabela, treino_validacao

HISTORICO = ["tempo_negocio_meses", "cliente_desde_meses",
             "emprestimos_anteriores"]
treino, valid = treino_validacao(tabela())
e = pd.read_csv("dados/brutos/emprestimos.csv")
cida = com_variaveis(e[e["cliente_id"] == "C00000"].tail(1))
grupos = {"só financeiras": FINANCEIRAS,
          "com o histórico": FINANCEIRAS + HISTORICO}
for nome, colunas in grupos.items():
    logistica = LogisticRegression(C=np.inf, tol=1e-10,
                                   max_iter=10_000)
    modelo = make_pipeline(StandardScaler(), logistica)
    modelo.fit(treino[colunas], treino["alvo"])
    p = modelo.predict_proba(cida[colunas])[0, 1]
    pv = modelo.predict_proba(valid[colunas])[:, 1]
    print(f"{nome:16} Dona Cida {p:6.1%}"
          f"  (acima de {(pv < p).mean():.0%})")
