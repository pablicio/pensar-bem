import matplotlib.pyplot as plt
import numpy as np

from mnist import carregar

imagens, rotulos = carregar("treino")
print("exemplos de treino por dígito:")
print(np.bincount(rotulos))

fig, eixos = plt.subplots(1, 10, figsize=(10, 1.4))
for d, ax in enumerate(eixos):
    media = imagens[rotulos == d].mean(axis=0)
    ax.imshow(media, cmap="gray_r")
    ax.set_title(str(d))
    ax.axis("off")
fig.tight_layout()
fig.savefig("medias.png", dpi=300)
