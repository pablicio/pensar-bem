import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from larga import tabela_larga

t, X = tabela_larga()
pca = PCA().fit(StandardScaler().fit_transform(X))
acumulada = np.cumsum(pca.explained_variance_ratio_)
for alvo in [0.5, 0.8, 0.95]:
    n = int(np.searchsorted(acumulada, alvo)) + 1
    print(f"{alvo:.0%} da variância: {n:2} componentes")
print(f"os dois do mapa: {acumulada[1]:.1%}")
