import numpy as np
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.tree import DecisionTreeRegressor

from risco.dados import tabela, treino_validacao
from risco.modelos import NUMERICAS

treino, valid = treino_validacao(tabela())
X, y = treino[NUMERICAS], treino["alvo"].to_numpy()
Xv, yv = valid[NUMERICAS], valid["alvo"].to_numpy()


def sigmoide(z):
    return 1 / (1 + np.exp(-z))


# o ponto de partida: o log da chance média, igual para todos
inicio = np.log(y.mean() / (1 - y.mean()))
F, Fv = np.full(len(y), inicio), np.full(len(yv), inicio)
PASSO = 2.0
print("árvores  perda no treino  AUC validação")
print(f"{0:7} {log_loss(y, sigmoide(F)):16.4f} {0.5:14.3f}")
for m in range(1, 201):
    residuo = y - sigmoide(F)      # o que falta acertar
    arvore = DecisionTreeRegressor(max_depth=2, random_state=0)
    arvore.fit(X, residuo)
    F += PASSO * arvore.predict(X)
    Fv += PASSO * arvore.predict(Xv)
    if m in (1, 2, 3, 10, 50, 200):
        perda = log_loss(y, sigmoide(F))
        auc = roc_auc_score(yv, Fv)
        print(f"{m:7} {perda:16.4f} {auc:14.3f}")
