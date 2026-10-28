import matplotlib.pyplot as plt
import numpy as np

pesos = np.load("pesos.npy")
w, b = pesos[:784].reshape(28, 28), pesos[784]
print(f"viés: {b:.0f}; pesos de {w.min():.1f} a {w.max():.1f}")
limite = np.abs(w).max()
fig, ax = plt.subplots(figsize=(3.2, 3.2))
ax.imshow(w, cmap="RdBu_r", vmin=-limite, vmax=limite)
ax.axis("off")
fig.tight_layout()
fig.savefig("pesos.png", dpi=500)
