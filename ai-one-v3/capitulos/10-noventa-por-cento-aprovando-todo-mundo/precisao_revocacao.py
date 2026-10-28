from sklearn.metrics import (confusion_matrix, precision_score,
                             recall_score)

from risco.dados import tabela, treino_validacao
from risco.modelos import COLUNAS, logistica

treino, valid = treino_validacao(tabela())
modelo = logistica().fit(treino[COLUNAS], treino["alvo"])
p = modelo.predict_proba(valid[COLUNAS])[:, 1]
yv = valid["alvo"]

corte = 0.15
recusa = (p >= corte).astype(int)
vn, fp, fn, vp = confusion_matrix(yv, recusa).ravel()
print(f"corte de {corte:.0%}: recusa {recusa.mean():.1%}")
print(f"  VP {vp:5,}   FP {fp:5,}")
print(f"  FN {fn:5,}   VN {vn:5,}")
print(f"precisão à mão:  {vp / (vp + fp):.3f}"
      f"   scikit-learn: {precision_score(yv, recusa):.3f}")
print(f"revocação à mão: {vp / (vp + fn):.3f}"
      f"   scikit-learn: {recall_score(yv, recusa):.3f}")
