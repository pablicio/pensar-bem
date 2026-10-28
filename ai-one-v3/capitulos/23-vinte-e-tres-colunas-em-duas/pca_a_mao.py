import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from larga import tabela_larga

t, X = tabela_larga()
print("colunas:", X.shape[1])
Z = StandardScaler().fit_transform(X)

# a matriz de covariância das colunas padronizadas
C = np.cov(Z, rowvar=False)
valores, vetores = np.linalg.eigh(C)
ordem = np.argsort(valores)[::-1]       # do maior para o menor
valores, vetores = valores[ordem], vetores[:, ordem]
explicada = valores / valores.sum()

pca = PCA().fit(Z)
sk = pca.explained_variance_ratio_
print("variância explicada pelos cinco primeiros:")
print("  à mão:       ", explicada[:5].round(3))
print("  scikit-learn:", sk[:5].round(3))
# o sinal de um autovetor é arbitrário: compara sem ele
iguais = np.allclose(np.abs(vetores.T),
                     np.abs(pca.components_))
print("mesmas direções:", iguais)
