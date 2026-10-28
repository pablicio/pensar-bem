import matplotlib.pyplot as plt
from sklearn.inspection import partial_dependence

from risco.campeao import COLUNAS_FINAIS, treinado
from risco.dados import lacrar, tabela
from risco.finalidade import com_divida

modelo = treinado()
aberto, _ = lacrar(com_divida(tabela()))
X = aberto[COLUNAS_FINAIS]
X = X.astype({"tempo_negocio_meses": float})  # pede float

fig, eixos = plt.subplots(1, 2, figsize=(9, 3.5), sharey=True)
for ax, coluna in zip(eixos, ["comprometimento",
                              "tempo_negocio_meses"]):
    pd_ = partial_dependence(modelo, X, [coluna],
                             response_method="predict_proba")
    grade, media = pd_["grid_values"][0], pd_["average"][0]
    ax.plot(grade, media)
    ax.set_xlabel(coluna)
    print(f"{coluna}: de {media.min():.1%}"
          f" a {media.max():.1%}")
eixos[0].set_ylabel("risco médio previsto")
fig.tight_layout()
fig.savefig("dependencia.png", dpi=300)
