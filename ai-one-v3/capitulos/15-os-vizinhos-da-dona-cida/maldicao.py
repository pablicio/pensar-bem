import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from risco.dados import tabela, treino_validacao
from risco.modelos import NUMERICAS

treino, valid = treino_validacao(tabela())
sorteio = np.random.default_rng(0)
print("colunas de ruído  AUC na validação")
for extras in [0, 10, 50, 200]:
    A = np.hstack([treino[NUMERICAS].to_numpy(),
                   sorteio.normal(size=(len(treino), extras))])
    B = np.hstack([valid[NUMERICAS].to_numpy(),
                   sorteio.normal(size=(len(valid), extras))])
    knn = KNeighborsClassifier(n_neighbors=101)
    modelo = make_pipeline(StandardScaler(), knn)
    modelo.fit(A, treino["alvo"])
    p = modelo.predict_proba(B)[:, 1]
    auc = roc_auc_score(valid["alvo"], p)
    print(f"{extras:17} {auc:17.3f}")
