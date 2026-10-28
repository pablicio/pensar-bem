import numpy as np
from sklearn.metrics import log_loss

from primeiro_modelo import FINANCEIRAS, primeiro_modelo
from risco.dados import tabela, treino_validacao

treino, valid = treino_validacao(tabela())
modelo = primeiro_modelo(treino)
p = modelo.predict_proba(valid[FINANCEIRAS])[:, 1]
taxa = treino["alvo"].mean()
chute = np.full(len(valid), taxa)
print(f"taxa de base do treino: {taxa:.3f}")
y = valid["alvo"]
print(f"perda log, chutando a taxa: {log_loss(y, chute):.4f}")
print(f"perda log, primeiro modelo: {log_loss(y, p):.4f}")
