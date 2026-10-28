import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC

# dois grupos pequenos, como duas carteiras bem diferentes
sorteio = np.random.default_rng(3)
bons = sorteio.normal([1.0, 1.0], 0.45, size=(20, 2))
maus = sorteio.normal([3.0, 2.6], 0.45, size=(20, 2))
X = np.vstack([bons, maus])
y = np.array([0] * 20 + [1] * 20)

fig, eixos = plt.subplots(1, 2, figsize=(9, 4), sharey=True)
for ax, C in zip(eixos, [100, 0.05]):
    svm = SVC(kernel="linear", C=C).fit(X, y)
    w, b = svm.coef_[0], svm.intercept_[0]
    largura = 2 / np.linalg.norm(w)
    n = len(svm.support_)
    print(f"C = {C:6}: {n:2} vetores de suporte,"
          f" margem de {largura:.2f}")
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm", s=25)
    s = svm.support_vectors_
    ax.scatter(s[:, 0], s[:, 1], s=120, facecolors="none",
               edgecolors="black")
    xs = np.linspace(0, 4, 50)
    for nivel, estilo in [(0, "-"), (-1, "--"), (1, "--")]:
        ax.plot(xs, (nivel - b - w[0] * xs) / w[1], estilo,
                color="gray")
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_title(f"C = {C}")
fig.tight_layout()
fig.savefig("margem.png", dpi=300)
