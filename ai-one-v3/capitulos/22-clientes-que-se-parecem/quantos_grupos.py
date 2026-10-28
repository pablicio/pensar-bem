import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from atrasos import PERFIL, atrasados

X = StandardScaler().fit_transform(atrasados()[PERFIL])
ks = range(2, 9)
inercias, silhuetas = [], []
print(" k   inércia  silhueta")
for k in ks:
    km = KMeans(k, n_init=10, random_state=0).fit(X)
    s = silhouette_score(X, km.labels_)
    inercias.append(km.inertia_)
    silhuetas.append(s)
    print(f"{k:2} {km.inertia_:9,.0f} {s:9.3f}")

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3.5))
a.plot(ks, inercias, marker="o")
a.set_title("inércia (cotovelo)")
b.plot(ks, silhuetas, marker="o")
b.set_title("silhueta média")
for ax in (a, b):
    ax.set_xlabel("número de grupos")
fig.tight_layout()
fig.savefig("cotovelo.png", dpi=300)
