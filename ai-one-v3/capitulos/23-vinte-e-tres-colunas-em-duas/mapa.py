import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from atrasos import PERFIL
from larga import tabela_larga

t, X = tabela_larga()
pca = make_pipeline(StandardScaler(), PCA(2))
pontos = pca.fit_transform(X)
# os quatro grupos do capítulo 22
grupos = make_pipeline(StandardScaler(),
                       KMeans(4, n_init=10, random_state=0))
t["grupo"] = grupos.fit_predict(t[PERFIL])

nomes = ["veteranos apertados", "novatos de começo",
         "reincidentes", "novatos de prazo longo"]
fig, ax = plt.subplots(figsize=(7, 5))
for g, nome in enumerate(nomes):
    p = pontos[t["grupo"] == g]
    ax.scatter(p[:, 0], p[:, 1], s=4, alpha=0.5, label=nome)
ax.set_xlabel("primeiro componente")
ax.set_ylabel("segundo componente")
ax.legend(markerscale=4)
fig.tight_layout()
fig.savefig("mapa.png", dpi=300)
