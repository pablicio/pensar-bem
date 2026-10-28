import numpy as np

from folha.conjunto import abre, parte, tabela

treino = [f for f in tabela()
          if parte(f["fazenda"]) == "treino"]
pixels = np.stack([abre(f["foto"]) for f in treino]) / 255
print("formato:", pixels.shape)
media = pixels.mean(axis=(0, 1, 2))
desvio = pixels.std(axis=(0, 1, 2))
print("média: ", np.round(media, 4))
print("desvio:", np.round(desvio, 4))
