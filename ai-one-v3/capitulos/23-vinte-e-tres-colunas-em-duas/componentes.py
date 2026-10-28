import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from larga import tabela_larga

t, X = tabela_larga()
Z = StandardScaler().fit_transform(X)
pca = PCA(n_components=2).fit(Z)
pesos = pd.DataFrame(pca.components_.T, index=X.columns,
                     columns=["pc1", "pc2"])
for pc in pesos:
    ordem = pesos[pc].abs().sort_values(ascending=False)
    maiores = ordem.index
    print(f"{pc}:")
    print(pesos.loc[maiores[:5], pc].round(2).to_string())
