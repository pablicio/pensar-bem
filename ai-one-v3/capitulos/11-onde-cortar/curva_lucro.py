import matplotlib.pyplot as plt
import numpy as np

from regra_jussara import regras_da_jussara
from risco.dados import tabela, treino_validacao
from risco.lucro import ganho, lucro
from risco.modelos import COLUNAS, logistica

treino, valid = treino_validacao(tabela())
modelo = logistica().fit(treino[COLUNAS], treino["alvo"])
p = modelo.predict_proba(valid[COLUNAS])[:, 1]
valores = ganho(valid)

cortes = np.arange(0.02, 0.51, 0.01)
lucros = np.array([lucro(p, valores, c) for c in cortes])
melhor = cortes[lucros.argmax()]
regra = regras_da_jussara(valid).all(axis=1).to_numpy()

politicas = [
    ("aprovar todo mundo", valores.sum(), 1.0),
    ("regra da Jussara", valores[regra].sum(), regra.mean()),
    ("logística, corte de 0.50", lucro(p, valores, 0.5),
     (p < 0.5).mean()),
    (f"logística, corte de {melhor:.2f}", lucros.max(),
     (p < melhor).mean()),
]
print("política                        lucro      aprova")
for nome, dinheiro, aprova in politicas:
    print(f"{nome:26} R$ {dinheiro:9,.0f} {aprova:9.0%}")

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(cortes, lucros / 1000)
ax.axvline(melhor, linestyle="--", color="gray")
ax.set_xlabel("corte: recusa acima desta probabilidade")
ax.set_ylabel("lucro na validação (mil R$)")
ax.set_title("O lucro de cada corte")
fig.tight_layout()
fig.savefig("lucro.png", dpi=300)
