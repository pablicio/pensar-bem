import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_auc_score

from risco.dados import tabela, treino_validacao
from risco.modelos import COLUNAS, boosting, logistica

treino, valid = treino_validacao(tabela())
# o último semestre do treino escolhe quando parar
ajuste = treino["data_concessao"] >= "2025-01-01"
antes, depois = treino[~ajuste], treino[ajuste]

modelo = boosting(iteracoes=1_500)
modelo.fit(antes[COLUNAS], antes["alvo"])
prepara, gb = modelo.named_steps.values()
X_depois = prepara.transform(depois[COLUNAS])
curva = [roc_auc_score(depois["alvo"], p[:, 1])
         for p in gb.staged_predict_proba(X_depois)]
melhor = int(np.argmax(curva)) + 1
print(f"melhor número de árvores: {melhor}"
      f" (AUC no ajuste {max(curva):.3f})")

final = boosting(iteracoes=melhor)
final.fit(treino[COLUNAS], treino["alvo"])
base = logistica().fit(treino[COLUNAS], treino["alvo"])
print()
for nome, m in [("logística", base), ("boosting", final)]:
    nota = m.predict_proba(valid[COLUNAS])[:, 1]
    auc = roc_auc_score(valid["alvo"], nota)
    print(f"{nome:9} AUC na validação {auc:.3f}")

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(range(1, len(curva) + 1), curva)
ax.axvline(melhor, color="gray", linestyle="--")
ax.set_xlabel("número de árvores")
ax.set_ylabel("AUC no ajuste")
fig.tight_layout()
fig.savefig("parada.png", dpi=300)
