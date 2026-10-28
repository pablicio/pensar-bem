import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss

from confiabilidade import balanceada, por_faixa
from risco.dados import tabela, treino_validacao
from risco.modelos import COLUNAS

treino, valid = treino_validacao(tabela())
inicio = pd.Timestamp("2025-01-01")
recente = treino["data_concessao"] >= inicio
antigo, calib = treino[~recente], treino[recente]
print(f"ajuste: {len(antigo):,}  calibração: {len(calib):,}"
      f"  validação: {len(valid):,}")

modelo = balanceada().fit(antigo[COLUNAS], antigo["alvo"])
p_cal = modelo.predict_proba(calib[COLUNAS])[:, 1]
p = modelo.predict_proba(valid[COLUNAS])[:, 1]
y = valid["alvo"].to_numpy()


def logit(p):
    return np.log(p / (1 - p)).reshape(-1, 1)


# Platt à mão: uma logística sobre o logit da probabilidade
platt = LogisticRegression(C=np.inf).fit(logit(p_cal),
                                         calib["alvo"])
a, b = platt.coef_[0, 0], platt.intercept_[0]
print(f"Platt: p' = sigmoide({a:.3f} x logit(p) {b:+.3f})")
p_platt = platt.predict_proba(logit(p))[:, 1]
calibradas = {"sem calibrar": p, "Platt à mão": p_platt}
for metodo in ["sigmoid", "isotonic"]:
    c = CalibratedClassifierCV(FrozenEstimator(modelo),
                               method=metodo)
    c.fit(calib[COLUNAS], calib["alvo"])
    calibradas[metodo] = c.predict_proba(valid[COLUNAS])[:, 1]

print("\nmétodo         Brier   média prevista")
for nome, q in calibradas.items():
    print(f"{nome:13} {brier_score_loss(y, q):.4f}"
          f"   {q.mean():13.1%}")
print(f"{'real':13}           {y.mean():13.1%}")

fig, ax = plt.subplots(figsize=(5, 5))
for nome in ["sem calibrar", "sigmoid"]:
    t = por_faixa(calibradas[nome], y)
    ax.plot(t["previsto"], t["real"], marker="o", label=nome)
ax.plot([0, 0.7], [0, 0.7], linestyle="--", color="gray",
        label="calibração perfeita")
ax.set_xlabel("probabilidade prevista")
ax.set_ylabel("fração que chegou a 90 dias")
ax.set_title("Diagrama de confiabilidade")
ax.legend()
fig.tight_layout()
fig.savefig("confiabilidade.png", dpi=300)
