import numpy as np
from sklearn.metrics import roc_auc_score

from risco.dados import tabela, treino_validacao
from risco.modelos import COLUNAS, boosting

treino, _ = treino_validacao(tabela())
ajuste = treino["data_concessao"] >= "2025-01-01"
antes, depois = treino[~ajuste], treino[ajuste]

print("taxa  melhor número  AUC no ajuste")
for taxa in [0.5, 0.05, 0.01]:
    modelo = boosting(iteracoes=3_000)
    modelo.set_params(modelo__learning_rate=taxa)
    modelo.fit(antes[COLUNAS], antes["alvo"])
    prepara, gb = modelo.named_steps.values()
    X_depois = prepara.transform(depois[COLUNAS])
    curva = [roc_auc_score(depois["alvo"], p[:, 1])
             for p in gb.staged_predict_proba(X_depois)]
    melhor = int(np.argmax(curva)) + 1
    print(f"{taxa:4} {melhor:14,} {max(curva):14.3f}")
