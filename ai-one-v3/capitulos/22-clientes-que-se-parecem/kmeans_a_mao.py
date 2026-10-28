import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from atrasos import PERFIL, atrasados

X = StandardScaler().fit_transform(atrasados()[PERFIL])
K = 4
sorteio = np.random.default_rng(0)
centros = X[sorteio.choice(len(X), size=K, replace=False)]

for passo in range(1, 101):
    # 1. cada ponto vai para o centro mais próximo
    dif = X[:, None, :] - centros[None, :, :]
    dist = (dif**2).sum(axis=2)
    grupo = dist.argmin(axis=1)
    inercia = dist[np.arange(len(X)), grupo].sum()
    # 2. cada centro vai para a média dos seus pontos
    novos = np.array([X[grupo == k].mean(axis=0)
                      for k in range(K)])
    if passo <= 3 or np.allclose(novos, centros):
        print(f"passo {passo:2}: inércia {inercia:9,.0f}")
    if np.allclose(novos, centros):
        break
    centros = novos

km = KMeans(K, n_init=10, random_state=0).fit(X)
print(f"\nscikit-learn:  inércia {km.inertia_:9,.0f}")
