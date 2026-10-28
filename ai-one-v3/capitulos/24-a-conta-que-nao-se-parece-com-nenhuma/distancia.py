from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

from recentes import COLUNAS, recentes

r = recentes()
colunas = COLUNAS + ["mesmo_telefone"]
Z = StandardScaler().fit_transform(r[colunas])
fone = r["telefone_referencia"]
golpe = (fone == "(71) 98877-1203").to_numpy()

for k in [5, 20]:
    # k + 1 vizinhos: o mais próximo de cada ponto é ele mesmo
    viz = NearestNeighbors(n_neighbors=k + 1).fit(Z)
    dist, _ = viz.kneighbors(Z)
    escore = dist[:, 1:].mean(axis=1)
    posicao = (-escore).argsort().argsort() + 1
    nove = posicao[golpe]
    print(f"k = {k:2}: as nove entre as posições"
          f" {nove.min():,} e {nove.max():,}")
