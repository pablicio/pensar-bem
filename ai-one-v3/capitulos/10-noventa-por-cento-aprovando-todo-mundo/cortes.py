from risco.dados import tabela, treino_validacao
from risco.modelos import COLUNAS, logistica

treino, valid = treino_validacao(tabela())
modelo = logistica().fit(treino[COLUNAS], treino["alvo"])
p = modelo.predict_proba(valid[COLUNAS])[:, 1]
yv = valid["alvo"].to_numpy()
print("corte  recusa  precisão  revocação")
for corte in [0.5, 0.3, 0.2, 0.15, 0.1]:
    recusa = p >= corte
    precisao = yv[recusa].mean()
    revocacao = recusa[yv == 1].mean()
    print(f"{corte:5.2f} {recusa.mean():7.1%} {precisao:9.1%}"
          f" {revocacao:10.1%}")
