import time

import numpy as np

from rio.texto import Vocabulario, mensagens, palavras, parte
from rio.vetores import pares, treina_vetores

treino = parte(mensagens(), "treino")["texto"]
voc = Vocabulario(treino, palavras)
c, _ = pares([voc.codifica(x) for x in treino])
print(f"{len(voc)} palavras, {len(c)} pares (centro, vizinho)")
inicio = time.time()
vetores = treina_vetores(voc, treino)
print(f"{time.time() - inicio:.0f} s; vetores {vetores.shape}")
np.save("vetores.npy", vetores)
