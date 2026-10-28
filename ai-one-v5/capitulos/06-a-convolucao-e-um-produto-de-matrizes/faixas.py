import matplotlib.pyplot as plt
import numpy as np

from folha.convolucao import toeplitz

K = np.arange(1, 10).reshape(3, 3)
T = toeplitz(K, 8)                      # imagem 8 × 8
print("T:", T.shape, f"· não zeros: {(T != 0).mean():.1%}")
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.imshow(np.where(T == 0, np.nan, T), cmap="viridis")
ax.set_xlabel("pixel da entrada (64)")
ax.set_ylabel("pixel da saída (36)")
fig.tight_layout()
fig.savefig("toeplitz.png", dpi=300)
