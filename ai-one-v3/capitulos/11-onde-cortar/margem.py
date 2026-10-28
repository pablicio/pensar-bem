import numpy as np

from risco.dados import tabela, treino_validacao
from risco.lucro import ganho, lucro
from risco.modelos import COLUNAS, logistica

treino, valid = treino_validacao(tabela())
modelo = logistica().fit(treino[COLUNAS], treino["alvo"])
p = modelo.predict_proba(valid[COLUNAS])[:, 1]
cortes = np.arange(0.02, 0.51, 0.01)
for margem in [0.3, 0.4, 0.5]:
    valores = ganho(valid, margem)
    lucros = [lucro(p, valores, c) for c in cortes]
    melhor = cortes[int(np.argmax(lucros))]
    print(f"margem de {margem:.0%}: melhor corte {melhor:.2f},"
          f" aprova {(p < melhor).mean():.0%}")
