import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (average_precision_score,
                             roc_auc_score,
                             roc_curve)

from risco.dados import tabela, treino_validacao
from risco.modelos import COLUNAS, logistica

treino, valid = treino_validacao(tabela())
modelo = logistica().fit(treino[COLUNAS], treino["alvo"])
p = modelo.predict_proba(valid[COLUNAS])[:, 1]
y = valid["alvo"].to_numpy()

# à mão: em quantos pares (mau, bom) o mau tem nota maior
maus, bons = p[y == 1], p[y == 0]
maior = (maus[:, None] > bons[None, :]).mean()
empate = (maus[:, None] == bons[None, :]).mean()
print(f"pares mau x bom: {len(maus) * len(bons):,}")
print(f"AUC à mão:       {maior + empate / 2:.4f}")
print(f"AUC sklearn:     {roc_auc_score(y, p):.4f}")
print(f"precisão média:  {average_precision_score(y, p):.4f}"
      f"   (taxa de base {y.mean():.4f})")

fpr, tpr, _ = roc_curve(y, p)
fig, ax = plt.subplots(figsize=(5, 5))
ax.plot(fpr, tpr, label="logística")
ax.plot([0, 1], [0, 1], linestyle="--", color="gray",
        label="sorteio")
ax.set_xlabel("bons recusados (taxa de falsos positivos)")
ax.set_ylabel("maus encontrados (revocação)")
ax.set_title("Curva ROC na validação")
ax.legend()
fig.tight_layout()
fig.savefig("roc.png", dpi=300)
