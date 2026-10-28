import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
from sklearn.metrics import roc_auc_score

from confiabilidade import balanceada
from risco.dados import tabela, treino_validacao
from risco.modelos import COLUNAS

treino, valid = treino_validacao(tabela())
inicio = pd.Timestamp("2025-01-01")
recente = treino["data_concessao"] >= inicio
antigo, calib = treino[~recente], treino[recente]
modelo = balanceada().fit(antigo[COLUNAS], antigo["alvo"])
y = valid["alvo"]
p = modelo.predict_proba(valid[COLUNAS])[:, 1]
print(f"sem calibrar  AUC {roc_auc_score(y, p):.4f}")
for metodo in ["sigmoid", "isotonic"]:
    c = CalibratedClassifierCV(FrozenEstimator(modelo),
                               method=metodo)
    c.fit(calib[COLUNAS], calib["alvo"])
    q = c.predict_proba(valid[COLUNAS])[:, 1]
    print(f"{metodo:13} AUC {roc_auc_score(y, q):.4f}")
