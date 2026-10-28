from risco.dados import tabela, treino_validacao
from risco.modelos import COLUNAS, logistica

treino, valid = treino_validacao(tabela())
modelo = logistica().fit(treino[COLUNAS], treino["alvo"])
p = modelo.predict_proba(valid[COLUNAS])[:, 1]
y = valid["alvo"].to_numpy()
for nome, aprova in [("aprova todo mundo", p < 1.1),
                     ("corte de 0.16", p < 0.16)]:
    taxa = y[aprova].mean()
    print(f"{nome:18} chegam a 90 dias: {taxa:.1%}")
